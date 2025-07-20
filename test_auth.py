import dash
from dash import html, dcc, Input, Output, State
import dash_bootstrap_components as dbc

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = dbc.Container([
    html.H1("인증 테스트", className="text-center mb-4"),
    
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

# 클라이언트 사이드 콜백
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

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8051) 