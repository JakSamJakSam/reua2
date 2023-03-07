function onFileChamge(e){
}
function imageInputInit(){
  const imageInputs = document.querySelectorAll('input[data-preview]');
  imageInputs.forEach((iInput) => {
    const id = iInput.id;
    const previewContainer = document.getElementById(`image_for_${id}`);
    if (previewContainer){
      iInput.addEventListener('change', () => {
          const file = iInput.files[0];
          const reader  = new FileReader();
          reader.onloadend = function () {
            previewContainer.style.background = `url(${reader.result}) center center no-repeat`
            previewContainer.style.backgroundSize = 'cover'
         }
       reader.readAsDataURL(file);
      });
    }
  })
}

imageInputInit();