/**
 * Created by zhangjun on 16/03/18.
 */

//add time plugin
$('#sandbox-container input').datepicker({
               language: 'zh-CN',
               autoclose: true,
	       format: 'yyyy-mm-dd',
               todayHighlight: true
           });
//   $('#sandbox-container input').datepicker("option", "disabled", true);

//history show info
function showHis(data) {
    var tbody = "";
    var host = "";
    $('#showModal').modal();
    $.getJSON("/webapp/history_api/",{'id':data},function(result){
    $.each(result, function(i, item){
    var trs = "";
      if (item == 'Success' || item == 'Failure') {
	trs += "<p style='word-break:break-all' class='bg-success'><strong>" + "Url:" + "</strong>" + "<br>" + i + "<br><br>" + "<strong>" + "检查结果:" + "</strong>" + "<br>" + item + "</p><br>";	
        tbody += trs;
	}
      else {
        host = "----------------分割线--------------<br>" + "<strong>" + "机器:" + "</strong>" + "<br>" + i + "<br>"
        $.each(item, function(k, v){
            if (v == 'OK') {
		trs += "<strong class='bg-success'>" + "检查结果:" + "</strong>" + "<br>" + v + "<br><br>";
	}
	    else {
            trs += "<p style='word-break:break-all' class='bg-success'><strong>" + "文件:" + "</strong>" + "<br>" + k + "<br><br>" + "<strong>" + "检查结果:" + "</strong>" + "<br>" + v + "<br></p><br>";
	}
	});
	    tbody += host;
            tbody += trs;
	}
      //else {
      //   trs += "<strong>" + "检测以线上为主(线上有,demo上缺少的目录)" + "</strong>" + "<br>" + "父目录:" + i + "<br><br>"  + "缺少的子目录:"+ "<br>" +"<p>" + item + "</p>"+ "<br>";
      //   tbody += trs;
	//}
     
    });
    //清空模态框的上一次数据
    $('p').empty();
    $("p").append(tbody);
})
};
