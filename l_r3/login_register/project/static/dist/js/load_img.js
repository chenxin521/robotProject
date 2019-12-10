function showImg(input) {
    var file = input.files[0];
    var reader = new FileReader()
    // 图片读取成功回调函数
    reader.onload = function (e) {
        document.getElementById('upload').src = e.target.result
    }
    reader.readAsDataURL(file)
}

// function showImg(input) {
//     var file = input.files[0];
//     var url = window.URL.createObjectURL(file)
//     document.getElemtById('upload').src = url
// }