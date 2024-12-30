
function onPageStart() {
    document.querySelectorAll('.arrow').forEach((element) => {
        const start_x = element.getAttribute("data-start-x")
        const start_y = element.getAttribute("data-start-y")
        const finish_x = element.getAttribute("data-finish-x")
        const finish_y = element.getAttribute("data-finish-y")
        console.log(start_x, start_y, finish_x, finish_y)
        const start = document.getElementById("cell-" + start_x + "-" + start_y)
        const finish = document.getElementById("cell-" + finish_x + "-" + finish_y)
        console.log(start.id, finish.id)
        rect = start.getBoundingClientRect()
        const start_center_disx =  rect.left + rect.width / 2;
        const start_center_disy = rect.top + rect.height / 2;
        rect = finish.getBoundingClientRect()
        const finish_center_disx = rect.left + rect.width / 2;
        const finish_center_disy = rect.top + rect.height / 2;
        path = element.children[1]
        path.setAttribute("d", 'M ' + start_center_disx + " " +  start_center_disy + " L " + finish_center_disx + " " + finish_center_disy)
    })
}

document.addEventListener('DOMContentLoaded', onPageStart);
window.addEventListener('resize', onPageStart);