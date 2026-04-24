import streamlit as st
import math

st.set_page_config(page_title="Scientific Calculator", page_icon="🧮")
st.title("🧮 Scientific Calculator")

# ── Session state ──────────────────────────────────────────────────────────────
if "expression" not in st.session_state:
    st.session_state.expression = ""
if "history" not in st.session_state:
    st.session_state.history = []

# ── Display ────────────────────────────────────────────────────────────────────
st.code(st.session_state.expression if st.session_state.expression else "0", language=None)

# ── Evaluate ───────────────────────────────────────────────────────────────────
def calculate(expr):
    try:
        expr = expr.replace("^", "**")

        # Build a safe math environment with degree-based trig
        safe_env = vars(math).copy()
        safe_env["sin"]       = lambda x: math.sin(math.radians(x))
        safe_env["cos"]       = lambda x: math.cos(math.radians(x))
        safe_env["tan"]       = lambda x: math.tan(math.radians(x))
        safe_env["asin"]      = lambda x: math.degrees(math.asin(x))
        safe_env["acos"]      = lambda x: math.degrees(math.acos(x))
        safe_env["atan"]      = lambda x: math.degrees(math.atan(x))
        safe_env["factorial"] = lambda x: math.factorial(int(x)) 

        result = eval(expr, {"__builtins__": {}}, safe_env)

        # Show as int if result is a whole number
        if isinstance(result, float) and result.is_integer():
            return int(result)
        return round(result, 10) if isinstance(result, float) else result
    except ZeroDivisionError:
        return "Error: Division by zero"
    except Exception:
        return "Error: Invalid expression"

# ── Number & operator buttons ──────────────────────────────────────────────────
st.markdown("### Basic")

rows = [
    [("7","7"),  ("8","8"),  ("9","9"),  ("➗","/")],
    [("4","4"),  ("5","5"),  ("6","6"),  ("✖","*")],
    [("1","1"),  ("2","2"),  ("3","3"),  ("➖","-")],
    [("0","0"),  (".","."),  ("(","("),  ("➕","+")],
    [(")",")"),  ("^","**"), ("%","*0.01"), ("√","sqrt(")],
]

for row in rows:
    cols = st.columns(4)
    for col, (label, token) in zip(cols, row):
        if col.button(label, key=f"basic_{token}", use_container_width=True):
            if "Error" in st.session_state.expression:
                st.session_state.expression = ""
            st.session_state.expression += token
            st.rerun()

# ── Control buttons ────────────────────────────────────────────────────────────
c1, c2, c3 = st.columns(3)

if c1.button("⌫", key="btn_back", use_container_width=True):
    st.session_state.expression = st.session_state.expression[:-1]
    st.rerun()

if c2.button("AC", key="btn_clear", use_container_width=True):
    st.session_state.expression = ""
    st.rerun()

if c3.button("=", key="btn_equals", use_container_width=True):
    result = calculate(st.session_state.expression)
    
    st.session_state.history.append(f"{st.session_state.expression} = {result}")
    st.session_state.history = st.session_state.history[-50:]

    
    if "Error" in str(result):
        st.session_state.expression = ""
    else:
        st.session_state.expression = str(result)

    st.rerun()


# ── Scientific functions ───────────────────────────────────────────────────────
st.markdown("---")

st.markdown("### Scientific")

sci_funcs = [
    ["sin(", "cos(", "tan(", "sqrt("],
    ["log10(", "log(", "exp(", "abs("],
    ["asin(", "acos(", "atan(", "factorial("],
    ["pi", "e", "**2", "^"],
]

for row in sci_funcs:
    cols = st.columns(4)
    for col, fn in zip(cols, row):
        # Use a unique key per button: prefix with "sci_"
        if col.button(fn, key=f"sci_{fn}", use_container_width=True):
            if "Error" in st.session_state.expression:
                st.session_state.expression = ""
            st.session_state.expression += fn
            st.rerun()

# ── Result display ─────────────────────────────────────────────────────────────
if st.session_state.expression:
    result = calculate(st.session_state.expression)
    st.info(f"**Result:** {result}")

# ── History ────────────────────────────────────────────────────────────────────
if st.session_state.history:
    st.markdown("---")
    st.markdown("### History")
    for item in reversed(st.session_state.history[-10:]):
        st.text(item)
    if st.button("Clear History", key="btn_clear_history"):
        st.session_state.history = []
        st.rerun()
