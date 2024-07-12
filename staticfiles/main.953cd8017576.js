//  form resetter ----------------------------------------------------------------------------------------------------
function clearForm(div_id) {
  var form = document.getElementById(div_id);
  form.reset();
}

//  previous page navigator ----------------------------------------------------------------------------------------------------
backBtn = document.getElementById("back-button");
backBtn.addEventListener("click", function (event) {
  event.preventDefault(); // Prevent the default anchor behavior
  window.history.go(-1); // Go back two pages
});

//  tabs controller ----------------------------------------------------------------------------------------------------
document.getElementById("defaultTab").click();
function openTab(event, tabName) {
  var i, tabcontent, tabBtn;
  tabcontent = document.getElementsByClassName("tabcontent");
  for (i = 0; i < tabcontent.length; i++) {
    tabcontent[i].style.display = "none";
  }
  tabBtn = document.getElementsByClassName("tabBtn");
  for (i = 0; i < tabBtn.length; i++) {
    tabBtn[i].className = tabBtn[i].className.replace(" active", "");
  }
  document.getElementById(tabName).style.display = "block";
  event.currentTarget.className += " active";
  var minitabs = document.getElementsByClassName("minitabcontent");
  if (minitabs.length != 0) {
    minitabs = tabcontent.children;
  }
}

//  accordions controller ----------------------------------------------------------------------------------------------------
function toggleAccordion(div_id) {
  var active_accordion = document.getElementById(div_id);
  var active_caret = document.getElementById(`${div_id}_caret`);

  // alert(div_id);

  if (active_accordion.classList.contains("hidden")) {
    for (let element of document.getElementsByClassName("accordion")) {
      element.classList.remove("block");
      element.classList.add("hidden");
    }
    for (let element of document.getElementsByClassName("fa-caret-down")) {
      element.classList.remove("rotate-180");
    }
    active_accordion.classList.remove("hidden");
    active_accordion.classList.add("block");
    active_caret.classList.add("rotate-180");
  } else {
    for (let element of document.getElementsByClassName("accordion")) {
      element.classList.remove("block");
      element.classList.add("hidden");
    }
    active_caret.classList.remove("rotate-180");
    active_accordion.classList.remove("block");
    active_accordion.classList.add("hidden");
  }
}

//  dropdown controller ----------------------------------------------------------------------------------------------------
function toggleMenu(e, obj_id) {
  activeMenu = document.getElementById(obj_id);
  e.name === `sentry`
    ? ((e.name = "close"), activeMenu.classList.remove("hidden"))
    : ((e.name = `sentry`), activeMenu.classList.add("hidden"));
}

//  pop up dismisser ----------------------------------------------------------------------------------------------------
window.addEventListener("mouseup", function (event) {
  activeMenu.classList.add("hidden");
});

//  selectfield dashes remover ----------------------------------------------------------------------------------------------------
$(document).ready(function () {
  // Add a placeholder option to the select element

  elements = document.getElementsByClassName("input_selector");
  elements.forEach((e) => {
    e.children().first().remove();
    $(".input_selector").prepend(
      '<option value="" disabled selected></option>'
    );
  });
});

 // ----------------------------pdf generator and exporter-------------------------------

  function generatePDF(div_id) {
  var doc = new jsPDF();
  html2canvas(document.getElementById(div_id))
    .then(canvas => {
      const imgData = canvas.toDataURL('image/png');
      doc.addImage(imgData, 'PNG', 0, 0);
      doc.save(`${div_id}.pdf`);
    });
  }

  // ----------------------------appointments exporter-------------------------------
function extractXLS (div_id) {
      document.getElementById(div_id);
      // Hide the "more_visits" row
      const moreRows = document.getElementById(`more${div_id}`);
      if (moreRows) {
        moreRows.style.display = "none";
      }
      // Create a new Excel workbook
      const wb = XLSX.utils.book_new();

      // Create a new worksheet
      const ws = XLSX.utils.table_to_sheet(
        document.getElementById(div_id)
      );
      // Add the worksheet to the workbook
      XLSX.utils.book_append_sheet(wb, ws, "Datasheet");

      // Save the workbook as an Excel file
      XLSX.writeFile(wb, "datasheet.xlsx");
    };
