function login() {
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    // 로그인 검증
    if (username === 'user' && password === 'pass') {
        window.location.href = '../../pages/home.html';  // 로그인 성공 시 홈 페이지로 이동
    } else {
        alert('유효한 정보가 아닙니다.');  // 팝업 경고창
    }
}