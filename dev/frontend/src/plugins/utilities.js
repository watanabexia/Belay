import axios from 'axios'

export default {
    install: (app, options) => {
        app.config.globalProperties.$isApiKeyExistsInCookie = function() {
            const apiKey = this.$cookies.get("api_key");
            return apiKey !== null && apiKey !== undefined;
        }

        const axiosInstance = axios.create({
            baseURL: 'http://127.0.0.1:5000/api',
            withCredentials: true
        })
        app.config.globalProperties.$axios = axiosInstance

        app.config.globalProperties.$getUsername = async function() {
            const response = await this.$axios.get('/users/me')
            return response.data["username"]
        }
    }
}