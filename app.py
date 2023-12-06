import streamlit as st
from chembl_webresource_client.new_client import new_client
from IPython.display import display
from ipywidgets import interact
import nglview as nv
import webbrowser
import os
import pandas as pd

def main():
    moleculeSearch()
    proteinSearch()

def moleculeSearch():
    st.image('chembl-img.png')
    st.title("CHEMBL SEARCH")
    search_molecule = st.text_input("Enter Molecule name:")
    if st.button("Search Molecule"):
        if search_molecule != "" or None:
            displayStructure(search_molecule)
        else:
            st.write("Not a valid search")

def displayStructure(search_molecule):
    try:
        molecule = new_client.molecule
        mols = molecule.filter(pref_name__iexact=search_molecule)
        st.write(f"Results for: {search_molecule}")
        st.write(f"Chemical Formula: {mols[0]['molecule_properties']['full_molformula']}")
        st.write(f"Smilies: {mols[0]['molecule_structures']['canonical_smiles']}")
        molecule_chembl_id = mols[0]['molecule_chembl_id']   
        image = new_client.image
        image.set_format('svg')
        svg_data = image.get(molecule_chembl_id)
        st.write(f"Molecular Visualization in 2D: ")
        st.image(svg_data, output_format='auto')
    except Exception as e:
        st.write("Not a valid search")

def proteinSearch():
    search_protein = st.text_input("Enter Amino acid Sequence:")
    if st.button("Search Protein"):
        if search_protein != "" or None:
            st.session_state["selected"] = None
            st.session_state["sequence"] = search_protein
            displayProtein()
        else:
            st.write("Not a valid search")
    data = {
        "Insulin": "GIVEQCCTSICSLYQLENYCN",
        "Hemoglobin": "VHLTPEEKSAVTALWGKVNVDEVGGEALGRLLVVYPWTQRFFESFGDLSTPDAVMGNPKVKAHGKKVLGAFSDGLAHLDNLKGTFATLSELHCDKLHVDPENFRLLGNVLVCVLAHHFGKEFTPPVQAAYQKVVAGVANALAHKYH",
        "Collagen": "GPPGPPGPPGPPGPPGPPGPPGPPG"
    }
    df = pd.DataFrame(data.items(), columns=["Protein", "Sequence"])
    st.write("Suggestions: ")
    st.table(df)
   
def displayProtein():
    os.system(f"curl -X POST --data {st.session_state['sequence']} https://api.esmatlas.com/foldSequence/v1/pdb/ > trial.pdb")    
    view = nv.show_structure_file('trial.pdb', gui=True)
    # view._set_sync_camera
    view._remote_call("setSize", target="widget", args=["500px", "500px"])
    view.center()
    view.render_image()
    nv.write_html('index.html', [view])
    webbrowser.open_new_tab('file://' + os.path.realpath('index.html'))

if __name__ == '__main__':
    main()