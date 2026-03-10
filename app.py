import streamlit as st
import streamlit.components.v1 as components
import os
import tempfile

from solver.QueenSolver import QueenSolver
from solver.Boards import BoardMode


# ------------------------------------------------
# Declare bidirectional component
# ------------------------------------------------

COMPONENT_DIR = os.path.join(tempfile.gettempdir(), "nqueens_component")
os.makedirs(COMPONENT_DIR, exist_ok=True)

with open(os.path.join(COMPONENT_DIR, "index.html"), "w") as f:
    f.write("""<!DOCTYPE html>
<html>
<head>
<style>
  * { margin:0; padding:0; box-sizing:border-box; }
  body { background:transparent; overflow:hidden; }
  [data-queen] { cursor:pointer; }
  [data-queen]:hover { filter: brightness(1.2); }
</style>
</head>
<body>
<div id="root"></div>
<script>
  var _lastClickId = null;   // tracks last sent click to avoid duplicates

  window.addEventListener("message", function(event) {
    if (event.data.type !== "streamlit:render") return;

    var args = event.data.args;
    document.getElementById("root").innerHTML = args.html;

    document.querySelectorAll("[data-queen]").forEach(function(el) {
      el.addEventListener("click", function() {
        var clickId = args.board_id + "_" + el.getAttribute("data-queen") + "_" + Date.now();
        _lastClickId = clickId;
        window.parent.postMessage({
          isStreamlitMessage: true,
          type: "streamlit:setComponentValue",
          value: {
            board_id: args.board_id,
            queen_idx: parseInt(el.getAttribute("data-queen")),
            click_id: clickId
          }
        }, "*");
      });
    });

    window.parent.postMessage({
      isStreamlitMessage: true,
      type: "streamlit:setFrameHeight",
      height: document.getElementById("root").scrollHeight + 4
    }, "*");
  });

  window.parent.postMessage({
    isStreamlitMessage: true,
    type: "streamlit:componentReady",
    apiVersion: 1
  }, "*");
</script>
</body>
</html>""")

_board_component = components.declare_component("nqueens_board", path=COMPONENT_DIR)

def queen_board(html, board_id, key=None):
    return _board_component(html=html, board_id=board_id, key=key, default=None)


# ------------------------------------------------
# Board HTML builder
# ------------------------------------------------

def build_board_html(solver, solution, selected_queen_idx=None):
    n, m = solver.n, solver.m

    highlight_set = set()
    if selected_queen_idx is not None:
        queen = solution[selected_queen_idx]
        blocked = solver.board.get_all_blocked_squares_queen(queen)
        highlight_set = set(map(tuple, blocked))

    queen_positions = {(q[0], q[1]): idx for idx, q in enumerate(solution)}
    cell_size = min(56, 420 // max(n, m))
    font_size = int(cell_size * 0.68)

    cells = []
    for i in range(n):
        for j in range(m):
            is_light = (i + j) % 2 == 0
            base = "#f0d9b5" if is_light else "#b58863"
            queen_idx = queen_positions.get((i, j))
            is_selected = queen_idx is not None and queen_idx == selected_queen_idx
            is_attacked = (i, j) in highlight_set

            if is_selected:
                bg = "#5ab552"
            elif is_attacked:
                bg = "#ff7f7f" if is_light else "#e05555"
            else:
                bg = base

            border = "box-shadow:inset 0 0 0 3px #1a5c16;" if is_selected else ""
            queen_attr = f'data-queen="{queen_idx}"' if queen_idx is not None else ""
            symbol = "&#9819;" if queen_idx is not None else ""

            cells.append(
                f'<div {queen_attr} style="width:{cell_size}px;height:{cell_size}px;'
                f'background:{bg};display:flex;align-items:center;justify-content:center;'
                f'font-size:{font_size}px;user-select:none;{border}">{symbol}</div>'
            )

    w, h = m * cell_size, n * cell_size
    grid = "".join(cells)
    return (
        f'<div style="display:inline-block;border:2px solid #444;line-height:0;">'
        f'<div style="display:grid;grid-template-columns:repeat({m},{cell_size}px);'
        f'width:{w}px;height:{h}px;">{grid}</div></div>'
    )


# ------------------------------------------------
# UI
# ------------------------------------------------

st.title("N-Queens Solver")

n = st.sidebar.number_input("Rows", 1, 20, 8)
m = st.sidebar.number_input("Columns", 1, 20, 8)
num_queens = st.sidebar.number_input("Number of queens", 1, max(n, m), min(n, m))
mode_name = st.sidebar.selectbox("Board type", [mode.name for mode in BoardMode])
mode = BoardMode[mode_name]
num_show = st.sidebar.number_input("Number of solutions to display", 1, 20, 5)
run_solver = st.sidebar.button("Solve")

if run_solver:
    solver = QueenSolver(n=n, m=m, num_queens=num_queens, mode=mode)
    solver.solve_problem()
    st.session_state["solver"] = solver
    st.session_state["solutions"] = solver.solutions
    for key in [k for k in st.session_state if k.startswith("queen_") or k.startswith("last_click_")]:
        del st.session_state[key]

# ------------------------------------------------
# Display solutions
# ------------------------------------------------

if "solutions" in st.session_state:

    solver = st.session_state["solver"]
    solutions = st.session_state["solutions"]

    st.write(f"**Total solutions found:** {len(solutions)}")
    st.caption("🖱️ Click a queen ♛ to highlight attacked squares. Click again to deselect.")

    for k, sol in enumerate(solutions[:num_show]):
        st.subheader(f"Solution {k + 1}")

        selected_idx = st.session_state.get(f"queen_{k}")
        html = build_board_html(solver, sol, selected_queen_idx=selected_idx)

        result = queen_board(html=html, board_id=k, key=f"board_{k}")

        if result is not None:
            click_id = result.get("click_id")
            last_id = st.session_state.get(f"last_click_{k}")

            if click_id != last_id:
                st.session_state[f"last_click_{k}"] = click_id
                clicked_queen = result["queen_idx"]
                if selected_idx == clicked_queen:
                    del st.session_state[f"queen_{k}"]
                else:
                    st.session_state[f"queen_{k}"] = clicked_queen
                st.rerun()