MODEL_CATALOG_START()

MODEL_TABLE_START("Tools" "See below a list of tools for tracking, calibration, and simulation." "Tools")
MODEL_TABLE_ROW(
  ID "Scalpel"
  DESCRIPTION "Generic scalpel (100mm long handle, 20mm long blade)."
  )
MODEL_TABLE_ROW(
  ID "Cautery"
  DESCRIPTION "Generic cautery (95mm long handle, 20mm long blade)."
  )
MODEL_TABLE_ROW(
  ID "Needle_BardDuaLok57"
  EDIT_LINK "${CATALOG_URL}/TrackingFixtures"
  DESCRIPTION "Bard DuaLok57 double-hook needle (without hooks)."
  )
MODEL_TABLE_ROW(
  ID "Stylus_100mm"
  PRINTABLE_FILES "TrackingFixtures/Stylus_100mm.stl"
  EDIT_LINK "${CATALOG_URL}/TrackingFixtures"
  DESCRIPTION "Pointer tool with built-in sensor holder. 100mm long, sharp tip."
  )
MODEL_TABLE_ROW(
  ID "Stylus_Candycane_100mm_WithHolder"
  PRINTABLE_FILES "TrackingFixtures/Stylus_Candycane_100mm_WithHolder.stl"
  EDIT_LINK "${CATALOG_URL}/TrackingFixtures"
  DESCRIPTION "Pointer tool with built-in sensor holder. 100mm long, curved tip for ultrasound calibration."
  )
MODEL_TABLE_ROW(
  ID "Stylus_Candycane_70mm_1.0"
  PRINTABLE_FILES "TrackingFixtures/Stylus_Candycane_70mm_1.0.stl"
  EDIT_LINK "${CATALOG_URL}/TrackingFixtures"
  DESCRIPTION "Pointer tool with built-in sensor holder. 70mm long, curved tip for ultrasound calibration."
  )
MODEL_TABLE_ROW(
  ID "UsProbe_SPL40"
  EDIT_LINK "${CATALOG_URL}/Tools/UsProbe_SPL40.par"
  DESCRIPTION "Mock linear ultrasound probe (width: 40mm)"
  )
MODEL_TABLE_ROW(
  ID "UsProbe_Ultrasonix_L14-5_38"
  DESCRIPTION "Ultrasonix L14-5/38 linear ultrasound probe."
  )
MODEL_TABLE_ROW(
  ID "UsProbe_Ultrasonix_C5-2_60"
  DESCRIPTION "Ultrasonix C5-2/60 curvilinear ultrasound probe."
  )
MODEL_TABLE_ROW(
  ID "UsProbe_Ultrasonix_EC9-5_10"
  DESCRIPTION "Ultrasonix EC9-5/10 endocavity curvilinear ultrasound probe."
  )
MODEL_TABLE_ROW(
  ID "UsProbe_Telemed_L12"
  DESCRIPTION "Telemed L12 linear ultrasound probe."
  )
# Add remaining experimental tools
SET(EXPERIMENTAL_TOOLS
  )
FOREACH(MODELFILE ${EXPERIMENTAL_TOOLS})
  MODEL_TABLE_ROW(ID ${MODELFILE} DESCRIPTION "Experimental")
ENDFOREACH()
MODEL_TABLE_END()

MODEL_TABLE_START("Tracking fixtures" "See below a list of fixtures that can be used for mounting tracker markers (both optical and electromagnetic) on various tools and objects." TrackingFixtures)
MODEL_TABLE_ROW(
  ID "Block4x4-ThreeHoles"
  DESCRIPTION "Block of solid material 40x40x14 mm size, with an extruded interface with three M4 holes 7 mm apart. The block can be edited to cut out an anatomical part, so the final product will interface with an anatomy."
  )
MODEL_TABLE_ROW(
  ID "CauteryGrabber"
  DESCRIPTION "New version for fixing a tracker to a cautery. For clamp tightening use hex-head cap screw, M6 thread, 30 mm long with a matching wing nut. For assembly with SensorHolder-OneHole use M4 bolt."
  )
MODEL_TABLE_ROW(
  ID "SensorHolder_Wing_1.0"
  DESCRIPTION "Clip to mount a MarkerHolder or 8mm Ascension EM sensor to an object. With a wing to make it easier to fix it by glue or screws."
  )
MODEL_TABLE_ROW(
  ID "Stylus_Polaris"
  DESCRIPTION "Optical marker with slots to insert NDI Polaris pegs to hold reflective spheres."
  PRINTABLE_FILES "TrackingFixtures/StealthStation/Stylus_Polaris.STL"
  )
MODEL_TABLE_ROW(
  ID "Ultrasound_Polaris"
  DESCRIPTION "Optical marker with slots to insert NDI Polaris pegs to hold reflective spheres."
  PRINTABLE_FILES "TrackingFixtures/StealthStation/Ultrasound_Polaris.STL"
  )
MODEL_TABLE_ROW(
  ID "MarkerHolder_120mm-even_long"
  DESCRIPTION "Holder for visible-light printed black&white optical tracker markers (such as MicronTracker)."
  PRINTABLE_FILES
    "TrackingFixtures/MarkerHolder_120mm-even_long.stl"
    "TrackingFixtures/Marker_01-04.pdf"
  )
MODEL_TABLE_ROW(
  ID "MarkerHolder_120mm-odd_long"
  DESCRIPTION "Holder for visible-light printed black&white optical tracker markers (such as MicronTracker)."
  PRINTABLE_FILES
    "TrackingFixtures/MarkerHolder_120mm-odd_long.stl"
    "TrackingFixtures/Marker_01-04.pdf"
  )
MODEL_TABLE_ROW(
  ID "MarkerHolder_120mm-even_short"
  DESCRIPTION "Holder for visible-light printed black&white optical tracker markers (such as MicronTracker)."
  PRINTABLE_FILES
    "TrackingFixtures/MarkerHolder_120mm-even_short.stl"
    "TrackingFixtures/Marker_01-04.pdf"
  )
MODEL_TABLE_ROW(
  ID "MarkerHolder_120mm-odd_short"
  DESCRIPTION "Holder for visible-light printed black&white optical tracker markers (such as MicronTracker)."
  PRINTABLE_FILES
    "TrackingFixtures/MarkerHolder_120mm-odd_short.stl"
    "TrackingFixtures/Marker_01-04.pdf"
  )
MODEL_TABLE_ROW(
  ID "NeedleClip-Assembly_16-20G"
  DESCRIPTION "Clamps to a needle of size 16-20 G through a sterile bag."
  )
MODEL_TABLE_ROW(
  ID "Telemed-MicrUs-L12-SensorHolder"
  IMAGE_PRINTABLE_FILE "TrackingFixtures/Telemed-MicrUs-L12-SensorHolder.stl"
  PRINTABLE_FILES
    "TrackingFixtures/TelemedHolder_L12_MarkedSide.stl"
    "TrackingFixtures/TelemedHolder-L12_UnmarkedSide.stl"
  DESCRIPTION "Parts for tracking Telemed MicrUs L12 ultrasound probe"
  )
MODEL_TABLE_ROW(
  ID "Telemed-L12-ClipOn"
  IMAGE_PRINTABLE_FILE "TrackingFixtures/Telemed-MicruUs-L12/Telemed-L12-ClipOn.stl"
  PRINTABLE_FILES
    "TrackingFixtures/Telemed-MicruUs-L12/Telemed-L12-ClipOn.STL"
  DESCRIPTION "A plastic holder for the Telemed L12 ultrasound probe, without moving parts."
  )
MODEL_TABLE_ROW(
  ID "GeMl615D_Clip_v01"
  IMAGE_FILE "TrackingFixtures/GE_ML6-15-D/GeMl615D_Clip_v01.png"
  PRINTABLE_FILES
    "TrackingFixtures/GE_ML6-15-D/GeMl615D_Clip_v01.STL"
  DESCRIPTION "Clip-on part for GE ML6-15-D ultrasound probe."
  )
MODEL_TABLE_ROW(
  ID "SensorHolder_2.0"
  DESCRIPTION "New sensor holder design. This will replace SensorHolder-Ordered_2mm_1.0 eventually. Holds either a Model 800 Ascension EM sensor, or another PLUS fixture, e.g. for holding MicronTracker markers. This part is frequently part of an assembly, but can also be used by itself."
  )
MODEL_TABLE_ROW(
  ID "SensorHolder-OneHole"
  DESCRIPTION "Holds a Model 800 sensor, and has a hole to fix to other printed components."
  )
MODEL_TABLE_ROW(
  ID "OrientationLR-Plane"
  DESCRIPTION "This is the most simple reference sensor holder to be used on patients. In a certain surgical setting (e.g. when stuck on the chest) this defines the patient orientation. This allows saving virtual camera positions."
  )
MODEL_TABLE_ROW(
  ID "PolarisAscensionPlane"
  IMAGE_PRINTABLE_FILE "TrackingFixtures/MultiModalityTracking/PolarisAscensionPlane.STL"
  PRINTABLE_FILES
    "TrackingFixtures/MultiModalityTracking/PolarisAscensionPlane.STL"
	"TrackingFixtures/MultiModalityTracking/PolarisAscensionPlane.rom"
  DESCRIPTION "Part that can be tracked by both Polaris and Ascension trackers"
  )
# Add remaining experimental tools
SET(EXPERIMENTAL_TRACKING_FIXTURES
  MarkerHolder_120mm_Winged_1.0
  MarkerHolder_120mm-Short_2.0
  NeedleGrabberFlappy-Assembly_1.0
  Plug-L_60mm_3.0
  SensorHolder-GlueHoles-Ordered_2mm_1.0
  SensorHolder-Ordered-HolesInterface_2mm_1.0
  )
FOREACH(MODELFILE ${EXPERIMENTAL_TRACKING_FIXTURES})
  MODEL_TABLE_ROW(ID ${MODELFILE} DESCRIPTION "Experimental")
ENDFOREACH()
MODEL_TABLE_END()

MODEL_TABLE_START("Calibration phantoms" "See below a list of ultrasound calibration phantoms." "fCalPhantom")
MODEL_TABLE_ROW(
  ID "fCal-2.0"
  IMAGE_FILE "fCalPhantom/fCal_2/PhantomDefinition_fCal_2.0_Wiring_2.0.png"
  PRINTABLE_FILES "fCalPhantom/fCal_2/fCal_2.0.stl"
  EDIT_LINK "${CATALOG_URL}/fCalPhantom/fCal_2"
  DESCRIPTION "Phantom for freehand spatial ultrasound calibration for shallow depth (up to 9 cm)."
  )
MODEL_TABLE_ROW(
  ID "fCal-2.1"
  PRINTABLE_FILES "fCalPhantom/fCal_2/fCal_2.1.stl"
  EDIT_LINK "${CATALOG_URL}/fCalPhantom/fCal_2"
  DESCRIPTION "Phantom for freehand spatial ultrasound calibration for shallow depth (up to 9 cm)."
  )
MODEL_TABLE_ROW(
  ID "fCal-3.1"
  IMAGE_FILE "fCalPhantom/fCal_3/fCal3.1.png"
  PRINTABLE_FILES
    "fCalPhantom/fCal_3/fCal_3.1.stl"
    "fCalPhantom/fCal_3/fCal_3.1_back.stl"
    "fCalPhantom/fCal_3/fCal_3.1_front.stl"
    "fCalPhantom/fCal_3/fCal_3.1_left.stl"
    "fCalPhantom/fCal_3/fCal_3.1_spacer.stl"
  EDIT_LINK "${CATALOG_URL}/fCalPhantom/fCal_3"
  DESCRIPTION "Phantom for freehand spatial ultrasound calibration for deep structures (up to 30 cm)."
  )
MODEL_TABLE_END()

MODEL_TABLE_START("Anatomy" "See below a list of anatomical models for simulation and testing." "Anatomy")
MODEL_TABLE_ROW(
  ID "HumanSimple"
  DESCRIPTION "Simple low-polygon human body model."
  )
MODEL_TABLE_ROW(
  ID "LumbarSpinePhantom"
  DESCRIPTION "Printable 3D model of the lumbar spine with matching CT image. Note that lowest vertebra is moved in the printable model compared to CT."
  PRINTABLE_FILES
    "Anatomy/LumbarSpinePhantom.stl"
    "Anatomy/LumbarSpinePhantom_CT.mha"
  )
MODEL_TABLE_END()

MODEL_CATALOG_END()
