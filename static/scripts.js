//runs tabs
function openTab(evt, action) {
  // Declare all variables
  var i, tabcontent, tablinks;

  //If view tab, dowload file
  if(action === 'View') {
    downloadFile()
  }

  // Get all elements with class="tabcontent" and hide them
  tabcontent = document.getElementsByClassName("tabcontent");
  for (i = 0; i < tabcontent.length; i++) {
    tabcontent[i].style.display = "none";
  }

  // Get all elements with class="tablinks" and remove the class "active"
  tablinks = document.getElementsByClassName("tablinks");
  for (i = 0; i < tablinks.length; i++) {
    tablinks[i].className = tablinks[i].className.replace(" active", "");
  }

  // Show the current tab, and add an "active" class to the button that opened the tab
  document.getElementById(action).style.display = "block";
  evt.currentTarget.className += " active";
}


//make file selector invisible
var input = document.querySelector('input');
var preview = document.querySelector('.preview');

//hide defult file selector input (because it can't be styled)
input.style.opacity = 0;

let curFiles = null;

//file input event listener
input.addEventListener('change', updateImageDisplay);

//update image display
function updateImageDisplay() {
  //Empty pervious content of the view
  while(preview.firstChild) {
    preview.removeChild(preview.firstChild);
  }

  //get all files selected
  curFiles = input.files;
  //If no files selected, add p element telling use no files selected
  if(curFiles.length === 0) {
    var para = document.createElement('p');
    para.textContent = 'No files currently selected for upload';
    preview.appendChild(para);
  } else {
    //If file is selected
    var list = document.createElement('ol');
    preview.appendChild(list);
    //for each file, add contents and size to view
    for(var i = 0; i < curFiles.length; i++) {
      var listItem = document.createElement('li');
      var para = document.createElement('p');
      para.textContent = 'File name ' + curFiles[i].name + ', file size ' + returnFileSize(curFiles[i].size) + '.';

      //check if file is pdf
      var image;
      // if(curFiles[i].type === 'application/pdf') {
        image = document.createElement('iframe');
      // } else {
      //   image = document.createElement('img');
      // }
      image.src = window.URL.createObjectURL(curFiles[i]);

      listItem.appendChild(image);
      listItem.appendChild(para);

      list.appendChild(listItem);

    }

  }
}

// console.log(curFiles);


//get file size
function returnFileSize(number) {
  if(number < 1024) {
    return number + 'bytes';
  } else if(number >= 1024 && number < 1048576) {
    return (number/1024).toFixed(1) + 'KB';
  } else if(number >= 1048576) {
    return (number/1048576).toFixed(1) + 'MB';
  }
}


//Dowloads and displays file downloaded from Box
function downloadFile(){
  //Get call to Dowload route to dowload the file
  fetch('/download')
  .then(response => response.json())
  .then(data => {

    // alert(data.success);

    view = document.getElementById('View');
    //If no file has been uploaded, tells user that
    if(data.success === 0) {

      let para = document.createElement('p');
      para.textContent = 'You have not uploaded an application'
      view.appendChild(para);

    } else {
      //If file has been uploaded, displays file
      let fileViewer = document.createElement('iframe');
      fileViewer.src = `static/${data.success}.pdf`;
      view.appendChild(fileViewer);
    }
  });
}

