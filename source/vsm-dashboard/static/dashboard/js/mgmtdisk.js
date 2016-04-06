
var $ctrlServer = $("#selServer")[0];
var $ctrlDisk = $("#selDisk")[0];
var USED_SIZE = 0
var DISK_TOTAL_SIZE = 0

var Server = {
	Create:function(){
		var server = {};
		server.name = $ctrlServer.options[$ctrlServer.selectedIndex].text;;
		server.node_id = $ctrlServer.options[$ctrlServer.selectedIndex].getAttribute("node-id");
		server.server_id = $ctrlServer.value;
		return server;
	}
}

var Disk = {
	Create:function(){
		var disk = {};
		disk.name = $ctrlServer.options[$ctrlServer.selectedIndex].text;
		return disk;
	}
}

var partition = {
	Create:function(){
		var part = {};
		part.name = $ctrlDisk.options[$ctrlDisk.selectedIndex].text + $("#txtNumber").val();
		part.number = $("#txtNumber").val();
		part.size = $("#txtNumber").val();
		part.start = "";
		part.end = "";
		part.type = $("#selParType").val();
		part.formattype = $("#selFormatType").val();
		return part;
	}
}

function ChangeServer(){
	//reset the add partition form
	ResetForm();
	server = Server.Create();
	PostData("get_disks_by_server",{"server_id":server.node_id});
}

function ChangeDisk(){
	//reset the add partition form
	ResetForm();
	disk = Disk.Create();
	PostData("get_parts_by_disk",{"disk_name":disk.name});
}

function UpdateSelDisks(disks){
	$("#selDisk")[0].options.length = 0;

	for(var i=0;i<disks.length;i++){
		var option1 = new Option();
		var option2 = new Option();
		option1.value = disks[i].size;
		option1.text = disks[i].name;
		$("#selDisk")[0].options.add(option1);
	}
	$("#selDisk")[0].selectedIndex = 0;
	DISK_TOTAL_SIZE = $("#selDisk").value();
}

function UpdateParForm(parts){
	$("#tbParList")[0].html("");
	USED_SIZE = 0
	for(var i=0;i<parts.length;i++){
	    USED_SIZE = USED_SIZE + parts[i].size;
		AddParItemToTable(parts[i]);
	}

}

function ClickAddParToTable(){
    var par = partition.Create();
    CheckParForm(par)
    AddParItemToTable(par);

}


function AddParItemToTable(part){
	var parHtml = "";
		parHtml += "<tr class=\"osd-item\">";
		parHtml += "	<td class='sortable normal_column'>"+part.name+"</td>";
		parHtml += "	<td class='sortable normal_column '>"+part.number+"</td>";
		parHtml += "	<td class='sortable normal_column '>"+part.start+"</td>";
		parHtml += "	<td class='sortable normal_column '>"+part.end +"</td>";
        parHtml += "	<td class='sortable normal_column '>"+part.size+"</td>";
		parHtml += "	<td class='sortable normal_column '>"+part.type+"</td>";
		parHtml += "	<td class='sortable normal_column '>"+part.format_type+"</td>";
		parHtml += "	<td class='sortable normal_column '>";
		parHtml += "		<button class=\"btn btn-danger\" onclick=\"RemoveOSD(this)\">Remove</button>";
		parHtml += "	</td>";
		parHtml += "</tr>";

	//check the empty row,and then remove
	if($("#trEmptyRow").length>0){
		$("#trEmptyRow").hide();
	}

	$("#tbParList").append(parHtml);
	USED_SIZE = USED_SIZE + part.size;
}

function RemovePar(obj){
	if(confirm("Are you sure that you want to remove this Partition?")){
		obj.parentNode.parentNode.remove();
		//check the table rows
		if($("#tbParList")[0].children.length == 1){
			$("#trEmptyRow").show();
		}
        USED_SIZE = USED_SIZE - obj.parentNode.parentNode[4].innerHTML;
	}	
}


function MgmtParsubmit(){
	var par_list = [];
	var PAR_Items = $(".par-item");
    if(PAR_Items.length == 0){
        showTip("error","Please add the Partition");
        return false;
    }

	for(var i=0;i<PAR_Items.length;i++){
		var par = {
		    "name":PAR_Items[i].children[1].innerHTML
			"number":PAR_Items[i].children[2].innerHTML,
			"size":PAR_Items[i].children[5].innerHTML,
            "start":PAR_Items[i].children[3].innerHTML,
			"end":PAR_Items[i].children[4].innerHTML,
			"type":PAR_Items[i].children[6].innerHTML,
			"format_type":PAR_Items[i].children[7].innerHTML
		}
		par_list.push(par);
	}

	var post_data = {
		"disk_name":[];
		"server_id":[];
		"parts":[];
	}

    var server_id = $ctrlServer.value;
    var disk_name = $ctrlServer.options[$ctrlServer.selectedIndex].text;

    post_data.disk_name = disk_name;
    post_data.server_id = server_id;
    post_data.parts = par_list;
    console.log(post_data);
    PostData("mgmt_parts_action",post_data);
}


function CheckParForm(par){
    if (USED_SIZE + par.size > DISK_TOTAL_SIZE)
    {
        showTip("error","The remaining disk space is not enough!");
		return  false;
    }

}


function ResetForm(){
	$("#txtNumber").val("");
	$("#txtSize").val("");
	$("#selParType")[0].selectedIndex = 0;
	$("#selFormatType")[0].selectedIndex = 0;
	$("#tbParList")[0].html("");
}

function PostData(method,postdata){
	var token = $("input[name=csrfmiddlewaretoken]").val();
	postData = JSON.stringify(postdata);

	$.ajax({
		type: "post",
		url: "/dashboard/vsm/partitions-mgmt/"+method+"/",
		data: postData,
		dataType:"json",
		success: function(data){
			switch(method){
				case "get_disks_by_server":
					UpdateSelDisks(data);
					break;
				case "get_parts_by_diak":
					UpdateParForm(data);
					break;
				case "mgmt_parts_action":
					if(data.status == "OK"){
						window.location.href = "/dashboard/vsm/partitions-mgmt/";
					}
					else{
						showTip("error",data.message);
					}	
					break;
			}
		},
		error: function (XMLHttpRequest, textStatus, errorThrown) {
			if(XMLHttpRequest.status == 500){
				showTip("error","Internal Error");
			}
		},
		headers: {
			"X-CSRFToken": token
		},
		complete: function(){

		}
    });
}
