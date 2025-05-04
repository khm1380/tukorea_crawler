const el = arguments[0];
const r = el.getBoundingClientRect();
const cx = r.left + r.width / 2, cy = r.top + r.height / 2;
['pointerover', 'pointerenter', 'mouseover', 'mousemove', 'pointerdown', 'mousedown', 'mouseup', 'click', 'pointerup'].forEach(type => {
    el.dispatchEvent(new MouseEvent(type, {
        view: window, bubbles: true, cancelable: true, clientX: cx, clientY: cy
    }));
});