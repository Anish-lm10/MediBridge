function showDoctorForm() {
    document.getElementById("doctor-form").style.display = "block";
    document.getElementById("patient-form").style.display = "none";
    document.getElementById("doctor-btn").classList.add("active");
    document.getElementById("patient-btn").classList.remove("active");
}

function showPatientForm() {
    document.getElementById("doctor-form").style.display = "none";
    document.getElementById("patient-form").style.display = "block";
    document.getElementById("patient-btn").classList.add("active");
    document.getElementById("doctor-btn").classList.remove("active");
}