// Basic drag-and-drop functionality
document.querySelectorAll('.unit').forEach(unit => {
    unit.addEventListener('dragstart', event => {
        event.dataTransfer.setData('text/plain', event.target.id);
    });
});

document.querySelectorAll('.cell').forEach(cell => {
    cell.addEventListener('dragover', event => {
        event.preventDefault();
    });

    cell.addEventListener('drop', event => {
        event.preventDefault();
        const unitId = event.dataTransfer.getData('text');
        const unit = document.getElementById(unitId);
        //const x = unit.getAttribute("data-x")
        //console.log(unit.getAttributeNames())
        //console.log(unit.getAttribute("class"))
        const y = cell.getAttribute("data-y")
        console.log(y)
        if (unit && !cell.childElementCount && y > 4) {
            cell.appendChild(unit);
        }
    });
});

const unplacedUnitsContainer = document.getElementById('unplaced-units');

unplacedUnitsContainer.addEventListener('dragover', event => {
    event.preventDefault();
});

unplacedUnitsContainer.addEventListener('drop', event => {
    event.preventDefault();
    const unitId = event.dataTransfer.getData('text');
    const unit = document.getElementById(unitId);

    if (unit) {
        unplacedUnitsContainer.appendChild(unit);
    }
});
