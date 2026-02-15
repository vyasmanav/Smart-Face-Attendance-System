const captureBtn = document.querySelector(".captureBtn")
const insertBtn = document.querySelector(".insertBtn")
const headers = { Authorization: 'Bearer ' + localStorage.getItem("token") }
const video = document.querySelector("#video");
const canvas = document.querySelector("#canvas")
const message = document.querySelector(".message")

async function capture(event) {
    event.preventDefault()
  if (navigator.mediaDevices.getUserMedia) {
    navigator.mediaDevices
      .getUserMedia({ video: true })
      .then(function (stream) {
        video.srcObject = stream;
      })
      .catch(function (error) {
        console.log("Something went wrong!");
      });
  }

  canvas.width = 200;
  canvas.height = 200;
  canvas.getContext("2d").drawImage(video, 0, 0, 200, 200);
  console.log(canvas.toDataURL());
}

async function insertData(event){
    event.preventDefault()
  dataURI = canvas.toDataURL();
  let pngBlob = dataURItoPNG(dataURI);
  console.log(pngBlob);
//   downloadPNG(pngBlob, "image.png");
  let imageFile = new File([pngBlob], "image.png");
  try {
    let data = await axios({
      method: "PATCH",
      url: `http://localhost:8000/manage-biometrics/`,
      data: {
        "face-image": imageFile
      },
      headers: {
        "Content-Type": "multipart/form-data",
        "Authorization": "Bearer " + localStorage.getItem("token")
      }
    })
    const html = `<div class="alert alert-success" role="alert">
    Success Uploaded
    </div>`
    message.innerHTML = ""
    message.insertAdjacentHTML("beforeend", html)
    console.log(data)
    console.log(data)
  } catch (error) {
    console.log(error)
    const html = `<div class="alert alert-primary" role="alert">
        <span id = "message" style="color:red">${error.response.data.message}</span>
        </div>`
        console.log(html)
        message.innerHTML = ""
        message.insertAdjacentHTML("beforeend", html)
  }
}

function dataURItoPNG(dataURI) {
  // convert base64 to raw binary data held in a string
  // doesn't handle URLEncoded DataURIs
  let byteString = atob(dataURI.split(",")[1]);

  // separate out the mime component
  let mimeString = dataURI.split(",")[0].split(":")[1].split(";")[0];

  // write the bytes of the string to an ArrayBuffer
  let ab = new ArrayBuffer(byteString.length);
  let ia = new Uint8Array(ab);
  for (let i = 0; i < byteString.length; i++) {
    ia[i] = byteString.charCodeAt(i);
  }

  // write the ArrayBuffer to a blob, and you're done
  let blob = new Blob([ab], { type: mimeString });
  return blob;
}

function downloadPNG(blob, filename) {
  // Create an object URL for the blob
  let url = URL.createObjectURL(blob);

  // Create a link element
  let link = document.createElement("a");
  link.download = filename;
  link.href = url;

  // Append the link to the body and click it
  document.body.appendChild(link);
  link.click();

  // Remove the link from the body
  document.body.removeChild(link);

  // Revoke the object URL
  URL.revokeObjectURL(url);
}


insertBtn.addEventListener("click",insertData)
captureBtn.addEventListener("click",capture)