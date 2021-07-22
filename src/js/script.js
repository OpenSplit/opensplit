global.closeAlert = function(event) {
    let element = event.target;
    while (element.nodeName !== "BUTTON") {
        element = element.parentNode;
    }
    element.parentNode.parentNode.removeChild(element.parentNode);
}
