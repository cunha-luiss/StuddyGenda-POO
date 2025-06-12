document.addEventListener('DOMContentLoaded', function() {
    // Password visibility toggle
    function togglePasswordVisibility() {
        const passwordField = document.getElementById("password");
        const toggleIcon = document.querySelector("#togglePassword i");
        const leftEye = document.querySelector(".left-eye");
        const rightEye = document.querySelector(".right-eye");
        
        if (passwordField && passwordField.type === "password") {
            passwordField.type = "text";
            if (toggleIcon) toggleIcon.className = "fas fa-eye-slash";
            if(leftEye) leftEye.style.transform = "scale(1.2)";
            if(rightEye) rightEye.style.transform = "scale(1.2)";
            leftEye.classList.add('active');
            rightEye.classList.add('active');
        } else if (passwordField) {
            passwordField.type = "password";
            if (toggleIcon) toggleIcon.className = "fas fa-eye";
            if(leftEye) leftEye.style.transform = "scale(1)";
            if(rightEye) rightEye.style.transform = "scale(1)";
            leftEye.classList.remove('active');
            rightEye.classList.remove('active');
        }
    }

    // Form validation
    function validateEmail(email) {
        const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return re.test(email);
    }

    function validatePassword(password) {
        return password.length >= 8;
    }

    function handleInput(inputField, errorElement, validationFunction) {
        const value = inputField.value;
        const isValid = validationFunction(value);
        
        if (isValid) {
            inputField.classList.remove("invalid");
            inputField.classList.add("valid");
            errorElement.classList.remove("visible");
        } else if (value) {
            inputField.classList.remove("valid");
            inputField.classList.add("invalid");
            errorElement.classList.add("visible");
        } else {
            inputField.classList.remove("valid", "invalid");
            errorElement.classList.remove("visible");
        }

        // Update robot eyes and mouth based on form validity
        updateRobotMood();
    }

    // Robot animation
    function updateRobotMood() {
        const emailInput = document.getElementById("email");
        const passwordInput = document.getElementById("password");
        
        // Check if elements exist before checking their classes
        const emailValid = emailInput && emailInput.classList.contains("valid");
        const passwordValid = passwordInput && passwordInput.classList.contains("valid");
        const emailInvalid = emailInput && emailInput.classList.contains("invalid");
        const passwordInvalid = passwordInput && passwordInput.classList.contains("invalid");
        
        const robotEyes = document.querySelectorAll(".eye");
        const robotMouth = document.getElementById("robot-mouth");
        
        // Only show happy face when both inputs are valid
        if (emailValid && passwordValid) {
            // Happy robot - smile curve (concave up)
            robotEyes.forEach(eye => eye.style.background = "#7eff84");
            if (robotMouth) {
                // Corrected smile curve - M45,63 Q60,73 75,63
                robotMouth.setAttribute("d", "M45,63 Q60,73 75,63");
                robotMouth.setAttribute("stroke-width", "2");
            }
        } 
        // Show sad face only when there's an invalid input (not empty inputs)
        else if (emailInvalid || passwordInvalid) {
            // Sad robot - frown curve (concave down)
            robotEyes.forEach(eye => eye.style.background = "#ff7e7e");
            if (robotMouth) {
                // Corrected frown curve - M45,58 Q60,48 75,58
                robotMouth.setAttribute("d", "M45,58 Q60,48 75,58");
                robotMouth.setAttribute("stroke-width", "2.5");
            }
        } 
        // Neutral face for empty or default state
        else {
            // Neutral robot - straight line
            robotEyes.forEach(eye => eye.style.background = "#4CAF50");
            if (robotMouth) {
                robotMouth.setAttribute("d", "M45,60 L75,60");
                robotMouth.setAttribute("stroke-width", "2");
            }
        }
    }

    // Event listeners
    const emailInput = document.getElementById("email");
    const passwordInput = document.getElementById("password");
    const emailError = document.getElementById("emailError");
    const passwordError = document.getElementById("passwordError");
    const togglePasswordBtn = document.getElementById("togglePassword");
    const toggleThemeBtn = document.getElementById("toggleTheme");
    const loginForm = document.getElementById("loginForm");

    if (emailInput && emailError) {
        emailInput.addEventListener("input", () => {
            handleInput(emailInput, emailError, validateEmail);
        });
        
        // Add blur event to show validation immediately when user leaves the field
        emailInput.addEventListener("blur", () => {
            if (emailInput.value) {
                handleInput(emailInput, emailError, validateEmail);
            }
        });
    }

    if (passwordInput && passwordError) {
        passwordInput.addEventListener("input", () => {
            handleInput(passwordInput, passwordError, validatePassword);
        });
        
        // Add blur event to show validation immediately when user leaves the field
        passwordInput.addEventListener("blur", () => {
            if (passwordInput.value) {
                handleInput(passwordInput, passwordError, validatePassword);
            }
        });
    }

    if (togglePasswordBtn) {
        togglePasswordBtn.addEventListener("click", togglePasswordVisibility);
    }

    if (toggleThemeBtn) {
        toggleThemeBtn.addEventListener("click", function() {
            document.documentElement.classList.toggle("light-mode");
            const icon = document.getElementById("themeIcon");
            if (document.documentElement.classList.contains("light-mode")) {
                icon.classList.remove("fa-moon");
                icon.classList.add("fa-sun");
            } else {
                icon.classList.remove("fa-sun");
                icon.classList.add("fa-moon");
            }
        });
    }

    if (loginForm) {
        loginForm.addEventListener("submit", function(e) {
            const isEmailValid = emailInput && validateEmail(emailInput.value);
            const isPasswordValid = passwordInput && validatePassword(passwordInput.value);
            
            if (isEmailValid && isPasswordValid) {
                // Simulate successful form submission
                const loginButton = document.querySelector(".login-button");
                loginButton.textContent = "Creating account...";
                loginButton.disabled = true;
                
                // Add success animation
                setTimeout(() => {
                    loginButton.textContent = "Account created! ✓";
                    loginButton.style.backgroundColor = "#2e7d32";
                    
                    // Animate robot for success - gentle smile
                    const robotEyes = document.querySelectorAll(".eye");
                    const robotMouth = document.getElementById("robot-mouth");
                    
                    robotEyes.forEach(eye => {
                        eye.style.transform = "scale(1.2)";
                        eye.style.background = "#7eff84";
                        eye.classList.add("active");
                    });
                    
                    if (robotMouth) {
                        // Big smile for success
                        robotMouth.setAttribute("d", "M45,63 Q60,73 75,63");
                        robotMouth.setAttribute("stroke-width", "2");
                    }
                }, 1500);
            } else {
                // Show validation errors
                if (!isEmailValid && emailInput && emailError) {
                    handleInput(emailInput, emailError, validateEmail);
                }
                if (!isPasswordValid && passwordInput && passwordError) {
                    handleInput(passwordInput, passwordError, validatePassword);
                }
                
                // Add small shake animation to indicate error
                loginForm.classList.add("shake");
                setTimeout(() => {
                    loginForm.classList.remove("shake");
                }, 500);
            }
        });
    }

    // Add hover effect to robot
    const robotContainer = document.querySelector(".robot-container");
    if (robotContainer) {
        robotContainer.addEventListener("mouseenter", function() {
            const eyes = document.querySelectorAll(".eye");
            eyes.forEach(eye => eye.classList.add("active"));
            
            // Small smile on hover, regardless of form state
            const robotMouth = document.getElementById("robot-mouth");
            if (robotMouth) {
                robotMouth.setAttribute("d", "M45,60 Q60,65 75,60");
            }
        });
        
        robotContainer.addEventListener("mouseleave", function() {
            const passwordField = document.getElementById("password");
            if (!passwordField || passwordField.type !== "text") {
                const eyes = document.querySelectorAll(".eye");
                eyes.forEach(eye => eye.classList.remove("active"));
            }
            
            // Return to appropriate expression based on form state
            updateRobotMood();
        });
    }

    // Initialize robot mouth as a straight line by default
    const robotSvg = document.querySelector("#robot");
    if (robotSvg) {
        const robotMouth = document.getElementById("robot-mouth");
        if (robotMouth) {
            robotMouth.setAttribute("d", "M45,60 L75,60");
            robotMouth.setAttribute("stroke-width", "2");
        }
    }

    // Initialize robot mood based on current form state
    // This ensures the robot smiles if the form is already valid
    updateRobotMood();
});
