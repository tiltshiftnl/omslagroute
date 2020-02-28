const fileUpload = document.getElementById( 'file-upload' );
const filesUploaded = document.getElementById( 'file-upload-filename' );

fileUpload.addEventListener( 'change', showFileName );

function showFileName( event ) {
    const input = event.srcElement;
    const fileName = input.files[0].name;
    filesUploaded.textContent = 'Geselecteerd bestand: ' + fileName;
}

if (document.addEventListener){
    document.addEventListener('invalid', function(e){
        e.target.className += ' invalid';
    }, true);
}