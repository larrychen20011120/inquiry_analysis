export function errorAlert() {
    let errorMsg = document.getElementsByClassName('error-msg');
    let showMsg = null;
    for (let i = 0; i < errorMsg.length; i++) {
        if (i == 0) {
            showMsg = errorMsg[0].textContent;
        } else {
            showMsg = showMsg.concat("\n", errorMsg[i].textContent);
        }
    }
    if (showMsg != null) {
        window.alert(showMsg);
    }
}
