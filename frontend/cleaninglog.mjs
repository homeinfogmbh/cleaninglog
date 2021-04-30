/*
    cleaninglog.mjs - Cleaning log JavaScript library.

    (C) 2021 HOMEINFO - Digitale Informationssysteme GmbH

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

    Maintainer: Richard Neumann <r dot neumann at homeinfo period de>
*/
'use strict';

import { suppressEvent } from 'https://javascript.homeinfo.de/lib.mjs';
import { request } from 'https://javascript.homeinfo.de/requests.mjs';

const URL = 'https://backend.homeinfo.de/cleaninglog-websubmit';
const CHECKBOX_VALUES = {
    'cleaning': "Reinigung",
    'gardening': "Garten",
    'maintenance': "Wartung"
};
const PARAMS = new URLSearchParams(window.location.search);


function *getAnnotations () {
    let checkbox;

    for (const id in CHECKBOX_VALUES) {
        checkbox = document.getElementById(id);

        if (checkbox.checked)
            yield CHECKBOX_VALUES[id];
    }

    const misc = document.getElementById('miscellaneous');
    const miscText = misc.value.trim();

    if (miscText != '')
        yield miscText;
}

function getAddress () {
    const street = PARAMS.get('s');
    const houseNumber = PARAMS.get('h');
    let address = '';

    if (street) {
        address += street;

        if (houseNumber)
            address += ' ' + houseNumber;
    }

    return address
}


function setAddress () {
    const address = getAddress();

    if (address)
        document.getElementById('address').innerHTML = address;
}


function getJSON (recaptchaResponse) {
    return {
        pin: document.getElementById('pin').value,
        deployment: parseInt(PARAMS.get('d')),
        annotations: Array.from(getAnnotations()),
        recaptchaResponse: recaptchaResponse
    };
}


function submit () {
    const recaptchaResponse = grecaptcha.getResponse();

    if (!recaptchaResponse)
        return alert('Bitte das reCAPTCHA lösen.');

    grecaptcha.reset();
    return request.post(URL, getJSON(recaptchaResponse)).then(
        () => alert('Reinigung eingetragen.'),
        () => alert('Fehler!.\nFalsche Zugangsdaten.')
    );
}


export function init (system) {
    const btnSubmit = document.getElementById('commit');
    btnSubmit.addEventListener('click', suppressEvent(submit), false);
    setAddress();
}
