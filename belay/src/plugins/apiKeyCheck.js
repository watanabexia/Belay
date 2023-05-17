export default {
    install: (app, options) => {
        app.config.globalProperties.$isApiKeyExistsInCookie = function() {
            const apiKey = this.$cookies.get("api_key");
            return apiKey !== null && apiKey !== undefined;
        }
    }
}