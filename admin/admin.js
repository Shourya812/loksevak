/* =========================================================
   LOKSAHAY ADMIN DASHBOARD
   Team Member 3 - Admin Dashboard
   ========================================================= */


/* =========================================================
   1. API CONFIGURATION
   ========================================================= */

const API_BASE_URL = "http://127.0.0.1:5000";


/* =========================================================
   2. DOM ELEMENTS
   ========================================================= */

// Mobile sidebar
const menuBtn = document.getElementById("menuBtn");
const sidebar = document.getElementById("sidebar");
const sidebarOverlay = document.getElementById("sidebarOverlay");

// Navigation
const dashboardNav = document.getElementById("dashboardNav");
const complaintsNav = document.getElementById("complaintsNav");

// Logout
const logoutBtn = document.getElementById("logoutBtn");

// Statistics
const totalComplaints =
    document.getElementById("totalComplaints");

const submittedCount =
    document.getElementById("submittedCount");

const underReviewCount =
    document.getElementById("underReviewCount");

const inProgressCount =
    document.getElementById("inProgressCount");

const resolvedCount =
    document.getElementById("resolvedCount");

// Complaints table
const complaintsTableBody =
    document.getElementById("complaintsTableBody");

// Complaint details modal
const complaintDetailsModal =
    document.getElementById("complaintDetailsModal");

const closeComplaintModal =
    document.getElementById("closeComplaintModal");

// Complaint details
const detailTitle =
    document.getElementById("detailTitle");

const detailCategory =
    document.getElementById("detailCategory");

const detailDescription =
    document.getElementById("detailDescription");

const detailLocation =
    document.getElementById("detailLocation");

const detailDate =
    document.getElementById("detailDate");

const detailStatus =
    document.getElementById("detailStatus");

const currentStatusDisplay =
    document.getElementById("currentStatusDisplay");

// Update status button
const updateStatusBtn =
    document.getElementById("updateStatusBtn");


/* =========================================================
   3. CURRENTLY SELECTED COMPLAINT
   ========================================================= */

let selectedComplaint = null;


/* =========================================================
   4. MOBILE SIDEBAR
   ========================================================= */

function openSidebar() {

    if (sidebar) {
        sidebar.classList.add("open");
    }

    if (sidebarOverlay) {
        sidebarOverlay.classList.add("show");
    }

}


function closeSidebar() {

    if (sidebar) {
        sidebar.classList.remove("open");
    }

    if (sidebarOverlay) {
        sidebarOverlay.classList.remove("show");
    }

}


if (menuBtn) {

    menuBtn.addEventListener("click", function () {

        openSidebar();

    });

}


if (sidebarOverlay) {

    sidebarOverlay.addEventListener("click", function () {

        closeSidebar();

    });

}


/* =========================================================
   5. NAVIGATION
   ========================================================= */

if (dashboardNav) {

    dashboardNav.addEventListener("click", function () {

        setActiveNavigation(dashboardNav);

        closeSidebar();

        window.scrollTo({
            top: 0,
            behavior: "smooth"
        });

    });

}


if (complaintsNav) {

    complaintsNav.addEventListener("click", function () {

        setActiveNavigation(complaintsNav);

        closeSidebar();

        const complaintsSection =
            document.querySelector(".complaints-section");

        if (complaintsSection) {

            complaintsSection.scrollIntoView({
                behavior: "smooth"
            });

        }

    });

}


function setActiveNavigation(activeItem) {

    const navigationItems =
        document.querySelectorAll(".nav-item");

    navigationItems.forEach(function (item) {

        item.classList.remove("active");

    });

    activeItem.classList.add("active");

}


/* =========================================================
   6. LOAD ALL COMPLAINTS
   ========================================================= */

async function loadComplaints() {

    try {

        showLoadingState();


        /*
         * IMPORTANT:
         * This is the actual endpoint confirmed
         * by the backend team.
         */

        const response = await fetch(
            `${API_BASE_URL}/api/admin/reports`
        );


        if (!response.ok) {

            throw new Error(
                `Server returned HTTP ${response.status}`
            );

        }


        const data =
            await response.json();


        console.log(
            "Admin reports response:",
            data
        );


        /*
         * The backend may return either:
         *
         * [
         *   {...},
         *   {...}
         * ]
         *
         * or:
         *
         * {
         *   reports: [...]
         * }
         *
         * Handle both forms.
         */

        let complaints = data;


        if (
            data &&
            !Array.isArray(data) &&
            Array.isArray(data.reports)
        ) {

            complaints = data.reports;

        }


        if (!Array.isArray(complaints)) {

            throw new Error(
                "Unexpected reports response format."
            );

        }


        displayComplaints(complaints);

        updateStatistics(complaints);


    } catch (error) {

        console.error(
            "Error loading complaints:",
            error
        );


        showEmptyState(
            "Unable to load complaints. Please check that the Flask backend is running."
        );


        updateStatistics([]);

    }

}


/* =========================================================
   7. LOADING STATE
   ========================================================= */

function showLoadingState() {

    if (!complaintsTableBody) {
        return;
    }


    complaintsTableBody.innerHTML = `

        <tr>

            <td
                colspan="7"
                class="table-message"
            >

                <div class="loading-state">

                    <div class="loading-icon">

                        <svg
                            viewBox="0 0 24 24"
                            fill="none"
                            stroke="currentColor"
                            stroke-width="2"
                        >

                            <path d="M12 2v4"></path>

                            <path d="M12 18v4"></path>

                            <path d="M4.93 4.93l2.83 2.83"></path>

                            <path d="M16.24 16.24l2.83 2.83"></path>

                            <path d="M2 12h4"></path>

                            <path d="M18 12h4"></path>

                        </svg>

                    </div>

                    <span>
                        Loading complaints...
                    </span>

                </div>

            </td>

        </tr>

    `;

}


/* =========================================================
   8. EMPTY STATE
   ========================================================= */

function showEmptyState(message) {

    if (!complaintsTableBody) {
        return;
    }


    complaintsTableBody.innerHTML = `

        <tr>

            <td
                colspan="7"
                class="table-message"
            >

                ${escapeHTML(message)}

            </td>

        </tr>

    `;

}


/* =========================================================
   9. DISPLAY COMPLAINTS
   ========================================================= */

function displayComplaints(complaints) {

    if (!complaintsTableBody) {
        return;
    }


    complaintsTableBody.innerHTML = "";


    if (
        !Array.isArray(complaints) ||
        complaints.length === 0
    ) {

        showEmptyState(
            "No complaints have been reported yet."
        );

        return;

    }


    complaints.forEach(function (complaint) {

        const row =
            document.createElement("tr");


        const status =
            complaint.status || "Submitted";


        /*
         * IMPORTANT:
         *
         * Backend uses:
         * address
         *
         * NOT:
         * location
         */

        const address =
            complaint.address || "—";


        row.innerHTML = `

            <td>
                ${escapeHTML(complaint.id)}
            </td>

            <td>
                ${escapeHTML(
                    complaint.title ||
                    "Untitled complaint"
                )}
            </td>

            <td>
                ${escapeHTML(
                    complaint.category ||
                    "—"
                )}
            </td>

            <td>
                ${escapeHTML(address)}
            </td>

            <td>
                ${escapeHTML(
                    formatDate(
                        complaint.created_at
                    )
                )}
            </td>

            <td>

                <span
                    class="status-badge ${getStatusClass(status)}"
                >
                    ${escapeHTML(status)}
                </span>

            </td>

            <td>

                <button
                    type="button"
                    class="view-btn"
                    data-id="${escapeHTML(complaint.id)}"
                >
                    View
                </button>

            </td>

        `;


        complaintsTableBody.appendChild(row);

    });


    attachViewButtonListeners();

}


/* =========================================================
   10. VIEW BUTTONS
   ========================================================= */

function attachViewButtonListeners() {

    const viewButtons =
        document.querySelectorAll(".view-btn");


    viewButtons.forEach(function (button) {

        button.addEventListener(
            "click",
            function () {

                const complaintId =
                    button.dataset.id;


                openComplaintDetails(
                    complaintId
                );

            }
        );

    });

}


/* =========================================================
   11. OPEN COMPLAINT DETAILS
   ========================================================= */

async function openComplaintDetails(complaintId) {

    try {

        /*
         * Use the backend's dedicated
         * single-report endpoint.
         */

        const response = await fetch(
            `${API_BASE_URL}/api/admin/reports/${complaintId}`
        );


        if (!response.ok) {

            throw new Error(
                `Server returned HTTP ${response.status}`
            );

        }


        const data =
            await response.json();


        console.log(
            "Single complaint response:",
            data
        );


        /*
         * Handle either:
         *
         * { ...complaint }
         *
         * or:
         *
         * { report: {...} }
         */

        let complaint = data;


        if (
            data &&
            data.report
        ) {

            complaint = data.report;

        }


        selectedComplaint =
            complaint;


        /* -------------------------
           Fill complaint details
           ------------------------- */

        detailTitle.textContent =
            complaint.title || "—";


        detailCategory.textContent =
            complaint.category || "—";


        detailDescription.textContent =
            complaint.description || "—";


        /*
         * Backend field is address.
         */

        detailLocation.textContent =
            complaint.address || "—";


        detailDate.textContent =
            formatDate(
                complaint.created_at
            );


        const status =
            complaint.status || "Submitted";


        detailStatus.value =
            status;


        if (currentStatusDisplay) {

            currentStatusDisplay.textContent =
                status;

        }


        /* -------------------------
           Show modal
           ------------------------- */

        complaintDetailsModal.classList.add(
            "show"
        );


        complaintDetailsModal.setAttribute(
            "aria-hidden",
            "false"
        );


    } catch (error) {

        console.error(
            "Error loading complaint details:",
            error
        );


        alert(
            "Unable to load complaint details."
        );

    }

}


/* =========================================================
   12. CLOSE COMPLAINT DETAILS
   ========================================================= */

function closeComplaintDetails() {

    if (complaintDetailsModal) {

        complaintDetailsModal.classList.remove(
            "show"
        );


        complaintDetailsModal.setAttribute(
            "aria-hidden",
            "true"
        );

    }


    selectedComplaint = null;

}


if (closeComplaintModal) {

    closeComplaintModal.addEventListener(
        "click",
        closeComplaintDetails
    );

}


if (complaintDetailsModal) {

    complaintDetailsModal.addEventListener(
        "click",
        function (event) {

            if (
                event.target ===
                complaintDetailsModal
            ) {

                closeComplaintDetails();

            }

        }
    );

}


/* =========================================================
   13. ESC KEY CLOSES MODAL
   ========================================================= */

document.addEventListener(
    "keydown",
    function (event) {

        if (
            event.key === "Escape" &&
            complaintDetailsModal &&
            complaintDetailsModal.classList.contains("show")
        ) {

            closeComplaintDetails();

        }

    }
);


/* =========================================================
   14. UPDATE COMPLAINT STATUS
   ========================================================= */

if (updateStatusBtn) {

    updateStatusBtn.addEventListener(
        "click",
        updateComplaintStatus
    );

}


async function updateComplaintStatus() {

    if (!selectedComplaint) {

        alert(
            "No complaint is currently selected."
        );

        return;

    }


    const complaintId =
        selectedComplaint.id;


    const newStatus =
        detailStatus.value;


    try {

        updateStatusBtn.disabled = true;


        const buttonText =
            updateStatusBtn.querySelector("span");


        if (buttonText) {

            buttonText.textContent =
                "Updating...";

        }


        /*
         * Actual backend endpoint:
         *
         * PUT /api/admin/reports/<id>/status
         */

        const response =
            await fetch(
                `${API_BASE_URL}/api/admin/reports/${complaintId}/status`,
                {
                    method: "PUT",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify({
                        status: newStatus
                    })
                }
            );


        const result =
            await response.json();


        console.log(
            "Status update response:",
            result
        );


        if (!response.ok) {

            throw new Error(
                result.message ||
                `Server returned HTTP ${response.status}`
            );

        }


        /*
         * Backend confirmed successful update.
         */

        selectedComplaint.status =
            newStatus;


        if (currentStatusDisplay) {

            currentStatusDisplay.textContent =
                newStatus;

        }


        alert(
            result.message ||
            "Complaint status updated successfully."
        );


        closeComplaintDetails();


        /*
         * Reload the complaints so that:
         *
         * - table status updates
         * - statistics update
         */

        await loadComplaints();


    } catch (error) {

        console.error(
            "Status update error:",
            error
        );


        alert(
            error.message ||
            "Unable to update complaint status."
        );


    } finally {

        updateStatusBtn.disabled = false;


        const buttonText =
            updateStatusBtn.querySelector("span");


        if (buttonText) {

            buttonText.textContent =
                "Update Status";

        }

    }

}


/* =========================================================
   15. UPDATE STATISTICS
   ========================================================= */

function updateStatistics(complaints) {

    if (!Array.isArray(complaints)) {

        complaints = [];

    }


    const submitted =
        complaints.filter(function (complaint) {

            return normalizeStatus(
                complaint.status
            ) === "submitted";

        }).length;


    const underReview =
        complaints.filter(function (complaint) {

            return normalizeStatus(
                complaint.status
            ) === "under review";

        }).length;


    const inProgress =
        complaints.filter(function (complaint) {

            return normalizeStatus(
                complaint.status
            ) === "in progress";

        }).length;


    const resolved =
        complaints.filter(function (complaint) {

            return normalizeStatus(
                complaint.status
            ) === "resolved";

        }).length;


    if (totalComplaints) {

        totalComplaints.textContent =
            complaints.length;

    }


    if (submittedCount) {

        submittedCount.textContent =
            submitted;

    }


    if (underReviewCount) {

        underReviewCount.textContent =
            underReview;

    }


    if (inProgressCount) {

        inProgressCount.textContent =
            inProgress;

    }


    if (resolvedCount) {

        resolvedCount.textContent =
            resolved;

    }

}


/* =========================================================
   16. STATUS CSS CLASS
   ========================================================= */

function getStatusClass(status) {

    const normalized =
        normalizeStatus(status);


    switch (normalized) {

        case "submitted":

            return "status-submitted";


        case "under review":

            return "status-review";


        case "in progress":

            return "status-progress";


        case "resolved":

            return "status-resolved";


        default:

            return "status-submitted";

    }

}


/* =========================================================
   17. NORMALIZE STATUS
   ========================================================= */

function normalizeStatus(status) {

    if (!status) {

        return "submitted";

    }


    return String(status)
        .trim()
        .toLowerCase();

}


/* =========================================================
   18. DATE FORMATTER
   ========================================================= */

function formatDate(dateValue) {

    if (!dateValue) {

        return "—";

    }


    const date =
        new Date(dateValue);


    if (isNaN(date.getTime())) {

        return String(dateValue);

    }


    return date.toLocaleString(
        "en-IN",
        {
            dateStyle: "medium",
            timeStyle: "short"
        }
    );

}


/* =========================================================
   19. BASIC HTML SAFETY
   ========================================================= */

function escapeHTML(value) {

    if (
        value === null ||
        value === undefined
    ) {

        return "";

    }


    const div =
        document.createElement("div");


    div.textContent =
        String(value);


    return div.innerHTML;

}


/* =========================================================
   20. LOGOUT
   ========================================================= */

if (logoutBtn) {

    logoutBtn.addEventListener(
        "click",
        function () {

            /*
             * Admin authentication has not been
             * defined by the backend yet.
             *
             * Therefore we do not invent a
             * logout/session system here.
             */

            alert(
                "Admin authentication/logout will be connected when the backend authentication system is finalized."
            );

        }
    );

}


/* =========================================================
   21. START DASHBOARD
   ========================================================= */

loadComplaints();