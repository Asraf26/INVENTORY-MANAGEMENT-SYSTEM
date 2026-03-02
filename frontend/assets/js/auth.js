// Authentication Module
const Auth = {
    currentUser: null,

    init() {
        const userData = localStorage.getItem('user');
        if (userData) {
            this.currentUser = JSON.parse(userData);
            // Update username in header
            const userName = document.getElementById('userName');
            if (userName && this.currentUser.username) {
                userName.textContent = this.currentUser.username;
            }
        }
    },

    setCurrentUser(user) {
        this.currentUser = user;
        localStorage.setItem('user', JSON.stringify(user));
        const userName = document.getElementById('userName');
        if (userName && user.username) {
            userName.textContent = user.username;
        }
    },

    getCurrentUser() {
        return this.currentUser;
    },

    isLoggedIn() {
        return !!this.currentUser;
    },

    logout() {
        localStorage.removeItem('user');
        localStorage.removeItem('loginTime');
        window.location.href = '/login.html';
    }
};
