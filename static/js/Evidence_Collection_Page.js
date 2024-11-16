document.addEventListener("DOMContentLoaded", function () {
    // Function to fetch and display case details
    async function fetchCaseDetails(caseId) {
        try {
            const response = await fetch(`/fetch-case-details/${caseId}`);
            const data = await response.json();

            if (response.ok) {
                // Populate the data into the HTML
                document.getElementById("caseId").textContent = data.caseId;
                document.getElementById("evidenceId").textContent = data.evidenceId;
                document.getElementById("crimeType").textContent = data.crimeType;
                document.getElementById("crimeDescription").textContent = data.crimeDescription;
                document.getElementById("evidenceDetails").textContent = data.evidenceDetails || "N/A";
                document.getElementById("crimeArea").textContent = data.crimeArea;
                document.getElementById("eyeWitnesses").textContent = data.witnesses || "N/A";
            } else {
                alert(data.error || "Failed to fetch case details.");
            }
        } catch (error) {
            console.error("Error fetching case details:", error);
            alert("An error occurred while fetching case details.");
        }
    }

    // Replace '3244' with the actual case ID you want to load dynamically
    const caseId = "3244";
    fetchCaseDetails(caseId);
});
