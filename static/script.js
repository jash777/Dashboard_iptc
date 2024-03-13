$(document).ready(function() {
    $("#apply-inbound-rule-btn").click(function() {
        var formData = {
            inbound_rule: {
                protocol: $("select[name='inbound_protocol']").val(),
                port: $("input[name='inbound_port']").val(),
                source_ip: $("input[name='inbound_source_ip']").val()
            }
        };

        $.ajax({
            url: '/apply-rules',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify(formData),
            success: function(response) {
                // Handle success response
                $("#response-message").html('<div class="alert alert-success" role="alert">Data added successfully!</div>');
                console.log(response);
            },
            error: function(xhr, status, error) {
                // Handle error response
                $("#response-message").html('<div class="alert alert-danger" role="alert">Error: ' + xhr.responseText + '</div>');
                console.error(xhr.responseText);
            }
        });
    });
});

function showSelectedIP() {
    var selectElement = document.getElementById("agent_ip");
    var selectedIP = selectElement.options[selectElement.selectedIndex].text;
    alert("Selected IP address: " + selectedIP);
}



$(document).ready(function() {
    $("#select-agent-btn").click(function() {
        var selectedAgent = $("#agent_ip").val();
        if (selectedAgent) {
            alert("Agent selected: " + selectedAgent);
        } else {
            alert("Please select an agent.");
            return;
        }
    });
});