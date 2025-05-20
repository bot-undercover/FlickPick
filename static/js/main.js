const param = new URLSearchParams(window.location.search)
const _prompt = param.get("prompt")
if (param.get("prompt") != null) {
fetch("/api?move=" + param.get("where") + "&data=" + prompt(_prompt, param.get("standart")))
window.location.replace(window.location.pathname)
};
const _alert = param.get("alert")
if (_alert != null) {
alert(_alert)
window.location.replace(window.location.pathname)
};