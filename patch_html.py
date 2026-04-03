import json

# Read the HTML file
html_path = 'templates/advisory/farm_input.html'
with open(html_path, 'r', encoding='utf-8') as f:
    html_content = f.read()

# Load the JSON
with open('indian_states_districts.json', 'r', encoding='utf-8') as f:
    json_data = f.read()

# Make the substitution in the HTML structure
# We need to change the <div class="col-md-6"> containing district 
# and add state right before it, making them col-md-4
# Let's find the location block:
search_str = """                            <div class="row g-4">
                                <div class="col-md-6">
                                    <div class="form-floating">
                                        {{ form.district }}"""

replace_str = """                            <div class="row g-4 align-items-end">
                                <div class="col-md-12 d-flex justify-content-end mb-n3" style="position: relative; top: 15px; z-index: 10;">
                                    <button type="button" id="liveLocationBtn" class="btn btn-sm btn-outline-success rounded-pill shadow-sm">
                                        <i class="fas fa-location-arrow me-1"></i> Use Live Location
                                    </button>
                                </div>
                                <div class="col-md-4">
                                    <div class="form-floating">
                                        {{ form.state }}
                                        <label for="{{ form.state.id_for_label }}" class="form-label">
                                            <i class="fas fa-map me-1"></i>{{ form.state.label }}
                                        </label>
                                    </div>
                                </div>
                                <div class="col-md-4">
                                    <div class="form-floating">
                                        {{ form.district }}"""

html_content = html_content.replace(search_str, replace_str)

# Change the crop col-md-6 to col-md-4
html_content = html_content.replace("""                                <div class="col-md-6">
                                    <div class="form-floating">
                                        {{ form.crop }}""", """                                <div class="col-md-4">
                                    <div class="form-floating">
                                        {{ form.crop }}""")

# Add the JavaScript at the end of the <script> block
js_to_add = f"""
    // Geolocation and dynamic dropdowns
    const statesData = {json_data}.states;
    const stateSelect = document.getElementById('id_state');
    const districtSelect = document.getElementById('id_district');
    
    // Initialize State dropdown
    if (stateSelect && statesData) {{
        // Keep the original options if any, or clear
        stateSelect.innerHTML = '<option value="">Select State</option>';
        statesData.forEach(stateObj => {{
            const option = document.createElement('option');
            option.value = stateObj.state;
            option.textContent = stateObj.state;
            stateSelect.appendChild(option);
        }});

        // Let's set default State if previously selected (for form errors)
        const selectedState = stateSelect.getAttribute('data-initial-val') || '';
        if (selectedState) {{
            stateSelect.value = selectedState;
        }}

        stateSelect.addEventListener('change', function() {{
            const selectedState = this.value;
            districtSelect.innerHTML = '<option value="">Select District</option>';
            
            if (selectedState) {{
                const stateInfo = statesData.find(s => s.state === selectedState);
                if (stateInfo) {{
                    stateInfo.districts.forEach(district => {{
                        const option = document.createElement('option');
                        option.value = district;
                        option.textContent = district;
                        districtSelect.appendChild(option);
                    }});
                }}
            }}
        }});
        
        // Trigger change initially to load districts if the state is selected
        if (stateSelect.value) {{
            stateSelect.dispatchEvent(new Event('change'));
        }}
    }}

    const liveLocationBtn = document.getElementById('liveLocationBtn');
    if (liveLocationBtn) {{
        liveLocationBtn.addEventListener('click', function() {{
            if ("geolocation" in navigator) {{
                const originalText = this.innerHTML;
                this.innerHTML = '<i class="fas fa-spinner fa-spin me-1"></i> Locating...';
                this.disabled = true;

                navigator.geolocation.getCurrentPosition(function(position) {{
                    const lat = position.coords.latitude;
                    const lon = position.coords.longitude;

                    fetch(`https://nominatim.openstreetmap.org/reverse?format=json&lat=${{lat}}&lon=${{lon}}&addressdetails=1`)
                        .then(response => response.json())
                        .then(data => {{
                            liveLocationBtn.innerHTML = originalText;
                            liveLocationBtn.disabled = false;

                            if (data && data.address) {{
                                const state = data.address.state;
                                const district = data.address.state_district || data.address.county || data.address.district;

                                if (state) {{
                                    Array.from(stateSelect.options).forEach(opt => {{
                                        if(opt.value.toLowerCase() === state.toLowerCase() || state.toLowerCase().includes(opt.value.toLowerCase())) {{
                                            stateSelect.value = opt.value;
                                            stateSelect.classList.add('is-valid');
                                        }}
                                    }});
                                    
                                    stateSelect.dispatchEvent(new Event('change'));

                                    if (district) {{
                                        setTimeout(() => {{
                                            Array.from(districtSelect.options).forEach(opt => {{
                                                const normalizedOpt = opt.value.toLowerCase().replace(' district', '');
                                                const normalizedDist = district.toLowerCase().replace(' district', '');
                                                if(normalizedOpt === normalizedDist || normalizedDist.includes(normalizedOpt)) {{
                                                    districtSelect.value = opt.value;
                                                    districtSelect.classList.add('is-valid');
                                                }}
                                            }});
                                        }}, 100);
                                    }}
                                }}
                            }}
                        }})
                        .catch(err => {{
                            console.error(err);
                            alert("Geocoding failed.");
                            liveLocationBtn.innerHTML = originalText;
                            liveLocationBtn.disabled = false;
                        }});
                }}, function(error) {{
                    console.error(error);
                    alert("Geolocation failed or denied.");
                    liveLocationBtn.innerHTML = originalText;
                    liveLocationBtn.disabled = false;
                }});
            }} else {{
                alert("Geolocation is not supported by your browser.");
            }}
        }});
    }}
"""

html_content = html_content.replace('});\n</script>', js_to_add + '\n});\n</script>')

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html_content)

print("Template patched successfully!")
