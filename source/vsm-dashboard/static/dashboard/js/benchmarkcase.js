//restart the osd
$("#benchmark_case_list__action_delete_benchmark_case").click(function(){
	var case_id_list = {"case_id_list":[]};

    var is_selected = false;
	$("#benchmark_case_list>tbody>tr").each(function(){
        if(this.children[0].children[0].checked) {
            is_selected = true;
            var case_id = this.children[0].children[0].value;
            case_id_list["case_id_list"].push(case_id);
        }
	});

    if(is_selected == false){
        showTip("warning","please select the case");
        return false;
    }

	token = $("input[name=csrfmiddlewaretoken]").val();
	$.ajax({
		type: "post",
		url: "/dashboard/vsm/benchmark_case/delete_benchmark_case/",
		data: JSON.stringify(case_id_list),
		dataType:"json",
		success: function(data){
				console.log(data);
                window.location.href= "/dashboard/vsm/benchmark_case/";
		   	},
		error: function (XMLHttpRequest, textStatus, errorThrown) {
				if(XMLHttpRequest.status == 500){
					$("#divOSDTip").show();
					$("#divOSDTip")[0].innerHTML = XMLHttpRequest.statusText;
				}
			},
		headers: {
			"X-CSRFToken": token
			},
		complete: function(){

		}
    });
	return false;
});