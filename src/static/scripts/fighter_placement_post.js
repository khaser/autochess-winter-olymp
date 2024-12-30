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
        const x = cell.getAttribute("data-x");
        const y = cell.getAttribute("data-y");
        console.log(y)
        if (unit && !cell.childElementCount && y > 4) {
            cell.appendChild(unit);
            const url = '/battles/planning';
            const textData = x + " " + y + " " + unit.getAttribute("id");
            const options = {
                method: 'POST',
                headers: {
                    'Content-Type': 'text/plain',
                },
                body: textData
            };

            fetch(url, options);
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
        const url = '/battles/planning';
        const textData = unit.getAttribute("id");
        const options = {
            method: 'POST',
            headers: {
                'Content-Type': 'text/plain',
            },
            body: textData
        };

        fetch(url, options);
    }
});
