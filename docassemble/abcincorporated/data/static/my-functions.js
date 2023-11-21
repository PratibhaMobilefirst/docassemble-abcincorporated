import variables_snapshot_connection,get_config, user_info, json from docassemble.base.util 

document.addEventListener('click', function(event) {
  if (event.target.classList.contains('reuse-button')) {
    var interviewId = event.target.dataset.interviewId;
    var modalContent = `
      <h2>Which document do you want to generate?</h2>
      <select id="which_doc">
        <option value="QDRO">QDRO</option>
        <option value="JOINDER">JOINDER</option>
      </select>
      <br><br>
      <button onclick="reuseInterview('${interviewId}')">Reuse</button>
    `;
    set_modal_content(modalContent);
    open_modal();
  }
});

function reuseInterview(interviewId) {
  var selectedOption = document.getElementById("which_doc").value;
  if (selectedOption !== "") {
    call_server('get_modal_content', { 'which_doc': selectedOption, 'interview_id': interviewId });
    close_modal();
  }
}

