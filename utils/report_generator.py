import os
from fpdf import FPDF
import datetime

class PDFReport(FPDF):
    def header(self):
        self.set_fill_color(0, 110, 181) # UN Blue
        self.rect(0, 0, 210, 15, 'F')
        self.set_text_color(255, 255, 255)
        self.set_font('Helvetica', 'B', 10)
        self.cell(0, 5, 'DevPulse AI | Executive Policy Brief', 0, 1, 'R')
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, 'Engineered by Abeera Ejaz | DevPulse AI Policy Engine', 0, 0, 'C')

def generate_policy_brief_pdf(country, baseline, simulated, sim_results, top_driver):
    pdf = PDFReport()
    pdf.add_page()
    
    # Title
    pdf.set_text_color(0, 51, 102)
    pdf.set_font('Helvetica', 'B', 18)
    pdf.cell(0, 10, f"Development Diagnostic & Policy Brief: {country}", ln=True)
    
    pdf.set_font('Helvetica', '', 10)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 6, f"Generated on: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')} | UN Framework Alignment", ln=True)
    pdf.ln(5)

    # Key Finding Box
    pdf.set_fill_color(240, 246, 255)
    pdf.set_text_color(0, 70, 130)
    pdf.set_font('Helvetica', 'B', 11)
    pdf.cell(0, 8, f" Primary Policy Priority: {top_driver}", fill=True, ln=True)
    pdf.ln(4)

    # Simulation Impact Summary
    pdf.set_font('Helvetica', 'B', 12)
    pdf.set_text_color(30, 30, 30)
    pdf.cell(0, 8, "Simulated Policy Outcomes:", ln=True)
    
    pdf.set_font('Helvetica', '', 10)
    pdf.cell(0, 6, f"- Baseline HDI: {sim_results['baseline_hdi']} ({sim_results['baseline_tier']})", ln=True)
    pdf.cell(0, 6, f"- Projected HDI: {sim_results['simulated_hdi']} ({sim_results['simulated_tier']}) [Growth: +{sim_results['hdi_pct_change']}%]", ln=True)
    pdf.cell(0, 6, f"- Baseline GDP per Capita: ${sim_results['baseline_gdp']:,}", ln=True)
    pdf.cell(0, 6, f"- Projected GDP per Capita: ${sim_results['simulated_gdp']:,} [Growth: +{sim_results['gdp_pct_change']}%]", ln=True)
    pdf.ln(5)

    # Indicator Comparison Table
    pdf.set_font('Helvetica', 'B', 10)
    pdf.set_fill_color(230, 230, 230)
    pdf.cell(80, 7, "Indicator", 1, 0, 'L', fill=True)
    pdf.cell(40, 7, "Baseline", 1, 0, 'C', fill=True)
    pdf.cell(40, 7, "Intervention Target", 1, 1, 'C', fill=True)

    pdf.set_font('Helvetica', '', 9)
    labels = {
        'Literacy_Rate_Adult_Pct': 'Adult Literacy Rate (%)',
        'Life_Expectancy_Years': 'Life Expectancy (Years)',
        'Access_to_Electricity_Pct': 'Electricity Access (%)',
        'Renewable_Energy_Pct': 'Renewable Energy Mix (%)',
        'Internet_Users_Pct': 'Internet Access (%)',
        'Infant_Mortality_Rate': 'Infant Mortality (per 1k)'
    }
    for k, label in labels.items():
        pdf.cell(80, 6, label, 1)
        pdf.cell(40, 6, str(round(baseline[k], 1)), 1, 0, 'C')
        pdf.cell(40, 6, str(round(simulated[k], 1)), 1, 1, 'C')

    output_path = os.path.join(os.path.dirname(__file__), '..', 'data', f"{country}_Policy_Brief.pdf")
    pdf.output(output_path)
    return output_path