/**
 * Created by Indexyz on 2017/1/19.
 */
$("#redirectPay").click(function () {
    $("#type").val(0)
});

$("#codePay").click(function () {
    $("#type").val(1);
});

$("#buyIframe").on('ready', function () {
    console.log(document.getElementById('buyIframe').contentWindow.location.href)
});

function change() {
    console.log("test")
}