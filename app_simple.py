import dash
from dash import html, dcc, Input, Output, State, dash_table, callback_context, ALL
import dash_bootstrap_components as dbc
import pandas as pd
import json
import os
from flask import Flask
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

# Flask 앱 설정
server = Flask(__name__)
server.config['SECRET_KEY'] = 'your-secret-key-here'

# Flask-Login 설정
login_manager = LoginManager()
login_manager.init_app(server)
login_manager.login_view = '/auth'

# Dash 앱 설정
app = dash.Dash(__name__, server=server, external_stylesheets=[dbc.themes.BOOTSTRAP])

# 사용자 관리
USER_FILE = 'users.json'

def load_users():
    if os.path.exists(USER_FILE):
        with open(USER_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_users(users):
    with open(USER_FILE, 'w', encoding='utf-8') as f:
        json.dump(users, f, ensure_ascii=False, indent=2)

class User(UserMixin):
    def __init__(self, id, password_hash):
        self.id = id
        self.password_hash = password_hash
    def get_id(self):
        return self.id

def get_user(user_id):
    users = load_users()
    if user_id in users:
        return User(user_id, users[user_id]['password_hash'])
    return None

@login_manager.user_loader
def user_loader(user_id):
    return get_user(user_id)

# 인증 레이아웃
def auth_layout():
    return dbc.Container([
        html.H1("로그인 또는 회원가입", className="text-center mb-4"),
        
        # 버튼들
        html.Div([
            dbc.Button("로그인", id="show-login", color="primary", className="me-2"),
            dbc.Button("회원가입", id="show-signup", color="secondary"),
        ], className="mb-3 text-center"),
        
        # 폼 컨테이너
        html.Div(id="form-container", children=[
            html.Div(id="login-form", children=[
                html.H4("로그인 폼"),
                html.P("로그인 폼입니다."),
                dbc.Input(id="login-username", placeholder="아이디", className="mb-2"),
                dbc.Input(id="login-password", type="password", placeholder="비밀번호", className="mb-2"),
                dbc.Button("로그인", id="login-button", color="primary")
            ]),
            html.Div(id="signup-form", style={"display": "none"}, children=[
                html.H4("회원가입 폼"),
                html.P("회원가입 폼입니다."),
                dbc.Input(id="signup-username", placeholder="아이디", className="mb-2"),
                dbc.Input(id="signup-password", type="password", placeholder="비밀번호", className="mb-2"),
                dbc.Input(id="signup-password-confirm", type="password", placeholder="비밀번호 확인", className="mb-2"),
                dbc.Button("회원가입", id="signup-button", color="success")
            ]),
        ]),
        
        # 메시지 영역
        html.Div(id="message", className="mt-3"),
        
    ], style={"maxWidth": "500px", "margin": "auto", "marginTop": "5vh"})

# 메인 레이아웃
def main_layout():
    return dbc.Container([
        html.H1("LCA 분석 시스템", className="text-center mb-4"),
        html.P("로그인에 성공했습니다!", className="text-center"),
        dbc.Button("로그아웃", id="logout-button", color="danger", className="mt-3"),
    ], style={"maxWidth": "800px", "margin": "auto", "marginTop": "5vh"})

# 앱 레이아웃
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

# 페이지 콜백
@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def display_page_content(pathname):
    if not current_user.is_authenticated and pathname != "/auth":
        return dcc.Location(href="/auth", id="force-auth-redirect")
    if pathname == "/auth":
        return auth_layout()
    return main_layout()

# 클라이언트 사이드 콜백 - 폼 전환
app.clientside_callback(
    """
    function(login_clicks, signup_clicks) {
        console.log('클라이언트 콜백 실행됨');
        console.log('login_clicks:', login_clicks);
        console.log('signup_clicks:', signup_clicks);
        
        if (login_clicks) {
            console.log('로그인 버튼 클릭됨');
            document.getElementById('login-form').style.display = 'block';
            document.getElementById('signup-form').style.display = 'none';
        } else if (signup_clicks) {
            console.log('회원가입 버튼 클릭됨');
            document.getElementById('login-form').style.display = 'none';
            document.getElementById('signup-form').style.display = 'block';
        }
        return window.dash_clientside.no_update;
    }
    """,
    Output("form-container", "children"),
    Input("show-login", "n_clicks"),
    Input("show-signup", "n_clicks"),
    prevent_initial_call=True
)

# 로그인 콜백
@app.callback(
    Output("message", "children"),
    Output("url", "pathname"),
    Input("login-button", "n_clicks"),
    State("login-username", "value"),
    State("login-password", "value"),
    prevent_initial_call=True
)
def handle_login(n_clicks, username, password):
    if not username or not password:
        return dbc.Alert("아이디와 비밀번호를 모두 입력해주세요.", color="danger"), "/auth"
    users = load_users()
    if username in users and check_password_hash(users[username]['password_hash'], password):
        user = User(username, users[username]['password_hash'])
        login_user(user)
        return "", "/"
    else:
        return dbc.Alert("아이디 또는 비밀번호가 올바르지 않습니다.", color="danger"), "/auth"

# 회원가입 콜백
@app.callback(
    Output("message", "children", allow_duplicate=True),
    Output("url", "pathname", allow_duplicate=True),
    Input("signup-button", "n_clicks"),
    State("signup-username", "value"),
    State("signup-password", "value"),
    State("signup-password-confirm", "value"),
    prevent_initial_call=True
)
def handle_signup(n_clicks, username, password, password_confirm):
    if not username or not password or not password_confirm:
        return dbc.Alert("모든 필드를 입력해주세요.", color="danger"), "/auth"
    if password != password_confirm:
        return dbc.Alert("비밀번호가 일치하지 않습니다.", color="danger"), "/auth"
    if len(password) < 6:
        return dbc.Alert("비밀번호는 최소 6자 이상이어야 합니다.", color="danger"), "/auth"
    users = load_users()
    if username in users:
        return dbc.Alert("이미 존재하는 아이디입니다.", color="danger"), "/auth"
    
    try:
        users[username] = {
            "password_hash": generate_password_hash(password),
            "created_at": str(pd.Timestamp.now())
        }
        save_users(users)
        user = User(username, users[username]['password_hash'])
        login_user(user)
        return dbc.Alert("회원가입이 완료되었습니다! 자동으로 로그인되었습니다.", color="success"), "/"
    except Exception as e:
        return dbc.Alert(f"회원가입 중 오류가 발생했습니다: {str(e)}", color="danger"), "/auth"

# 로그아웃 콜백
@app.callback(
    Output("url", "pathname", allow_duplicate=True),
    Input("logout-button", "n_clicks"),
    prevent_initial_call=True
)
def handle_logout(n_clicks):
    logout_user()
    return "/auth"

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8052) 