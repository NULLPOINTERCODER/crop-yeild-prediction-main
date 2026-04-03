# Patching templates/advisory/farm_input.html for crop changes
import json

html_path = 'templates/advisory/farm_input.html'
with open(html_path, 'r', encoding='utf-8') as f:
    html_content = f.read()

# 1. Add the manual_crop field to the HTML structure
# We'll put it in a new row right after the first location row
crop_search_str = """                                <div class="col-md-4">
                                    <div class="form-floating">
                                        {{ form.crop }}
                                        <label for="{{ form.crop.id_for_label }}" class="form-label">
                                            <i class="fas fa-seedling me-1"></i>{{ form.crop.label }}
                                        </label>
                                    </div>
                                </div>"""

crop_replace_str = crop_search_str + """
                                <div class="col-md-12" id="manualCropRow" style="display: none;">
                                    <div class="form-floating">
                                        {{ form.manual_crop }}
                                        <label for="{{ form.manual_crop.id_for_label }}" class="form-label">
                                            <i class="fas fa-edit me-1"></i>{{ form.manual_crop.label }}
                                        </label>
                                    </div>
                                    <small class="text-muted ms-2 mt-1 d-block"><i class="fas fa-info-circle me-1"></i> Please specify the exact crop name for better advice</small>
                                </div>"""

html_content = html_content.replace(crop_search_str, crop_replace_str)

# 2. Add the JavaScript for toggling and filtering
# We'll insert it before the closing script tag.
# Since I don't have a giant mapping for all districts, I'll provide a framework.
js_to_add = """
    // Manual Crop Toggle and District Filtering
    const cropSelect = document.getElementById('id_crop');
    const manualCropRow = document.getElementById('manualCropRow');
    const manualCropInput = document.getElementById('id_manual_crop_input');

    if (cropSelect && manualCropRow) {
        cropSelect.addEventListener('change', function() {
            if (this.value === 'other') {
                manualCropRow.style.display = 'block';
                manualCropInput.required = true;
            } else {
                manualCropRow.style.display = 'none';
                manualCropInput.required = false;
            }
        });
        
        // Initial state
        if (cropSelect.value === 'other') {
            manualCropRow.style.display = 'block';
            manualCropInput.required = true;
        }
    }

    // District-based Crop Suggestions (Expansion Logic)
    // Here we define which crops are "Recommended" for certain districts.
    // Districts not listed will show the default list.
    const districtCropMapping = {
        'bhubaneswar': ['rice', 'maize', 'other'],
        'cuttack': ['rice', 'mung', 'other'],
        'angul': ['maize', 'cotton', 'other'],
        'balasore': ['rice', 'groundnut', 'other'],
        'puri': ['rice', 'groundnut', 'other'],
        'sambalpur': ['rice', 'sugarcane', 'other'],
        // This mapping can be expanded with more data from the ML dataset if needed
    };

    const originalCropOptions = Array.from(cropSelect.options).map(opt => ({
        value: opt.value,
        text: opt.innerText
    }));

    if (districtSelect && cropSelect) {
        districtSelect.addEventListener('change', function() {
            const district = this.value.toLowerCase();
            const recommendedCrops = districtCropMapping[district];

            if (recommendedCrops) {
                // Clear and repopulate with ONLY recommended crops
                cropSelect.innerHTML = '<option value="">Select Crop</option>';
                originalCropOptions.forEach(opt => {
                    if (recommendedCrops.includes(opt.value)) {
                        const newOpt = document.createElement('option');
                        newOpt.value = opt.value;
                        newOpt.innerText = opt.text;
                        cropSelect.appendChild(newOpt);
                    }
                });
            } else {
                // Show all if no specific mapping
                cropSelect.innerHTML = '<option value="">Select Crop</option>';
                originalCropOptions.forEach(opt => {
                    const newOpt = document.createElement('option');
                    newOpt.value = opt.value;
                    newOpt.innerText = opt.text;
                    cropSelect.appendChild(newOpt);
                });
            }
        });
    }
"""

html_content = html_content.replace('});\n</script>', js_to_add + '\n});\n</script>')

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html_content)

print("Template updated for crop filtering and manual entry!")
