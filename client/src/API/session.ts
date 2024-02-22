export async function getToken() {
    // check if there is a token in local storage
    const token = localStorage.getItem('token');
    if (token) {
        return token;
    }
    // if there isn't, return null
    return null;
}