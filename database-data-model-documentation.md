# Data Model


## Data Model Description

The project features two data models:

- **daschland** model: Focuses on the narrative of Alice in Wonderland.
- **project-metadata** model: Hosts the materials used to create the project and its documentation.

Both models leverage all class and property types available on the DaSCH Service Platform (DSP). They are fully documented (with comments at both class and property levels) and designed to showcase DSP’s features. While most of the project is publicly accessible, certain classes and properties are private to demonstrate DSP’s access control capabilities.

The **daschland** data model is built around the stories of Alice in Wonderland and Through the Looking Glass and what Alice found there:

- **Story** : An ObjectWithoutRepresentation class, linked to **Book Chapters**. It includes a private **Alternative Description** property to illustrate DSP’s access control.
- **Book Chapter** : contains all **Story** subdivisions (chapters, introductions, poems). The **Alternative Description** property is private, to reflect the possibilities of DSP. The Richtext property **Description** of non-chapter resources (e.g. the Poem "All in the Golden Afternoon" (BCH_001)) includes **Comments**. A **Gallery Viewer** displays images from the original edition.
- **Location** is a superclass with two classes. The type of the class is ObjectWithoutRepresentation. Each resource of the class is a place that appeared in one of the two stories. The Richtext property **Description** illustrates the possibility of multiple cardinalities and contains descriptions in the four languages of the project, each of them being an instance of the property.

    - **Real world,** dedicated to the places that exist in our worldfeaturing the Geoname property.
    - **Wonderland,** contains fictional locations from the stories.

- **Event** is as well a super class, of type ObjectWithoutRepresentation. The class **Event** contains a richttext property named **Description** that contains **standoff links** towards the class **Location** and the **Character** of Alice. Four subclasses depend on this class, and inherit all its properties:
    
    - **Conflict**
    - **Adventure**
    - **Social**
    - **Alternative** has its accessibility set to private, in order showcase DSP’s access control.

- **Character** contains a property for **Alternative Description** that is private, in order showcase DSP’s access control. The Richtext property **Description** contains **Footnotes (e.g.** "Alice" (CH_001), "Jabberwock" (CH_026)). The class contains a **Gallery viewer**.
- **Image** is a StillImageRepresentation class. It is also the superclass to two subclasses. **Annotations** are drawn on several images: the flamingo and the white rabbit are annotated each time they appear on an image, each with a specific colour. The concerned images are gathered in one Link Object called **Image_Annotations**. These annotations are also the place where the **Color** property can be found.
    
    - **Image Original**
    - **Image Alternative:** blurred, to demonstrate DSP’s limited-view feature.

- **Book Cover** contain iiif Images stored on external servers. The link to the servers is mentionned in a URI Property.
- **Edition** is a DocumentRepresentation class and contain pdf that are directly readable.
- **Video** is a MovingImageRepresentation class. Video segments can be found in the video, illustrating this feature of DSP.
- **Audio** is an AudioRepresentation class. Audio segments can be found in two resources (“Dramatis Personae” (A_01); “Down the Rabbit-Hole” (A_02))

The **project-metadata** data model contains files that were used to create the project, as well as the documentation about the project, the database and a user guide on how to search the database.

- **Material** is a TextDocument class containing the original files used to import the data of the project on DSP.
- **Archive** is an ArchiveDocument class that hosts an Archive file, which contains all data that cannot be stored in another class.
- **Project Documentation** is meant to contain pdf versions of the project documentation (including this documnent).


## Controlled Vocabularies

The vocabularies reflect DSP’s capabilities and are available in English and French (with German and Italian possible):

- **Event type** is hierarchical and has three levels. It serves to classify the resources of the class Events.
- **Keyword** is hierarchical and has four levels. It is present in several parts of the Database.
- **License** is a flat list containing licence names. Its purpose is to provide legal information to all resources of all classes.
- **Role** is a flat list containing only two values. Its purpose is to classify the characters as main or secondary.

## Choice of External Mappings
The data models are mapped to established ontologies:

- FOAF (xmlns.com/foaf/0.1/)
- DCMI Terms (purl.org/dc/terms/)
- Schema (schema.org)
- Cidoc-CRM (cidoc-crm.org)

This mapping ensures reusability and provides a template for other projects, though some redundancy may exist.
