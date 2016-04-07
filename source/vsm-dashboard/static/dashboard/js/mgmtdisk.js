
var $ctrlServer = $("#selServer")[0];
var $ctrlDisk = $("#selDisk")[0];
var $ctrlParType = $("#selParType")[0];
var $ctrlFormatType = $("#selFormatType")[0];
var USED_SIZE = 0
var DISK_TOTAL_SIZE = 0
var submit_data = {"to_remove":[],"to_add":[],"to_format":[]}
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
		disk.name = $ctrlDisk.options[$ctrlDisk.selectedIndex].text;
		disk.size = $ctrlDisk.options[$ctrlDisk.selectedIndex].value;
		return disk;
	}
}

var partition = {
	Create:function(){
		var part = {};
		part.name = $ctrlDisk.options[$ctrlDisk.selectedIndex].text + $("#txtNumber").val();
		part.number = $("#txtNumber").val();
		part.size = $("#txtSize").val();
		part.start = "";
		part.end = "";
		part.type = $ctrlParType.options[$ctrlParType.selectedIndex].text;
		part.format_type = $ctrlFormatType.options[$ctrlFormatType.selectedIndex].text;
		return part;
	}
}
function CovertSizeToKB(size_str){
    var size_int = 0
    if (size_str.indexOf("M") != -1){
        size_int = parseInt(size_str)*1000
    }
    else if(size_str.indexOf("G") != -1){
        size_int = parseInt(size_str)*1000*1000
    }
    else if(size_str.indexOf("T") != -1){
        size_int = parseInt(size_str)*1000*1000*1000
    }
    else{
        size_int = parseInt(size_str)
    }
    return size_int
}
$(function(){
    UpdateSelFormatType();
    UpdateSelParType();
});

function ChangeNewFormat(obj){
    var part_number = obj.parentNode.parentNode.childNodes[3].innerHTML;
    var new_format_type = obj.options[obj.selectedIndex].text;
    for (i=0;i<submit_data.to_format.length;i++){
        if (submit_data.to_format[i].number == part_number){
            submit_data.to_format.pop(i);
        }
    }
    submit_data.to_format.push({"number":part_number,"new_format":new_format_type});
}

function ChangeServer(){
	//reset the add partition form
	ResetForm();
	server = Server.Create();
	PostData("get_disks_by_server",{"server_id":server.node_id});
	ChangeDisk();
}

function ChangeDisk(){
	//reset the add partition form
	ResetForm();
	server = Server.Create();
	disk = Disk.Create();
	DISK_TOTAL_SIZE = CovertSizeToKB(disk.size);
	PostData("get_parts_by_disk",{"disk_name":disk.name,
	"server_id":server.node_id});
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
	DISK_TOTAL_SIZE = CovertSizeToKB($("#selDisk")[0][0].value);
}

function UpdateParForm(parts){
	$("#tbParList").html("");
	USED_SIZE = 0
	for(var i=0;i<parts.length;i++){
	    USED_SIZE = USED_SIZE + CovertSizeToKB(parts[i].size);
	    parts[i].flag = 'old';
		AddParItemToTable(parts[i]);
	}

}
function UpdateSelFormatType(){
	$("#selFormatType")[0].options.length = 0;
    format_types = ["--","xfs","ext4"]
	for(var i=0;i<format_types.length;i++){
		var option1 = new Option();
		option1.value = i;
		option1.text = format_types[i];
		$("#selFormatType")[0].options.add(option1);
	}
	$("#selFormatType")[0].selectedIndex = 0;
}

function UpdateSelParType(){
	$("#selParType")[0].options.length = 0;
    part_types = ["primary","extended","logical"]
	for(var i=0;i<part_types.length;i++){
		var option1 = new Option();
		option1.value = i;
		option1.text = part_types[i];
		$("#selParType")[0].options.add(option1);
	}
	$("#selParType")[0].selectedIndex = 0;
}

function ClickAddParToTable(){
    var par = partition.Create();
    CheckParForm(par);
    par.flag = 'new';
    AddParItemToTable(par);
    submit_data.to_add.push(par);

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
		parHtml += "	<td class='sortable normal_column '>"
		parHtml += "	    <select id='selNewFormat_" + part.number +"' class='form-control' style='width: 100px;' onchange='ChangeNewFormat(this)'>"
        parHtml += "            <option value = ''  >--</option>"
        parHtml += "            <option value = ''  >xfs</option>"
        parHtml += "            <option value = ''  >ext4</option>"
        parHtml += "	    </select></td>"
        parHtml += "	<td class='sortable normal_column hidden '>"+part.flag+"</td>";
		parHtml += "	<td class='sortable normal_column '>";
		parHtml += "		<button class=\"btn btn-danger\" onclick=\"RemoveOSD(this)\">Remove</button>";
		parHtml += "	</td>";
		parHtml += "</tr>";
	//check the empty row,and then remove
	if($("#trEmptyRow").length>0){
		$("#trEmptyRow").hide();
	}

	$("#tbParList").append(parHtml);
	USED_SIZE = USED_SIZE + CovertSizeToKB(part.size);
}

function RemovePar(obj){
	if(confirm("Are you sure that you want to remove this Partition?")){
		var removed_flag = obj.parentNode.parentNode.childNodes[17].innerHTML;
		var removed_number = obj.parentNode.parentNode.childNodes[3].innerHTML;
        if (removed_flag=='old'){
            submit_data.to_remove.push({'number':removed_number})
        }
        else if(removed_flag=='new'){
            for (i=0;i<submit_data.to_add.length;i++){
                if (submit_data.to_add[i].number == removed_number){
                    submit_data.to_add.pop(i);
                    break
                }
            }
        }
        USED_SIZE = USED_SIZE - CovertSizeToKB(obj.parentNode.parentNode.childrenNodes[9].innerHTML);
		obj.parentNode.parentNode.remove();
		//check the table rows
		if($("#tbParList")[0].children.length == 1){
			$("#trEmptyRow").show();
		}
	}
}


function MgmtParsubmit(){
	server = Server.Create();
	disk = Disk.Create();
    submit_data.server_id = server.node_id;
    submit_data.disk_name = disk.name;
    PostData("mgmt_parts_action",submit_data);
}


function CheckParForm(par){
    if (USED_SIZE + CovertSizeToKB(par.size) > DISK_TOTAL_SIZE)
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
	$("#tbParList").html("");
	submit_data = {"to_remove":[],"to_add":[],"to_format":[]}

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
				case "get_parts_by_disk":
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
