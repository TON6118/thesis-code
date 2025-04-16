# -*- coding: mbcs -*-
from part import *
from material import *
from section import *
from assembly import *
from step import *
from interaction import *
from load import *
from mesh import *
from optimization import *
from job import *
from sketch import *
from visualization import *
from connectorBehavior import *
import os
import shutil
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import time
import numpy as np
from abaqusConstants import *
import random
import csv


start_time = time.time()
#creating new directory in base_directory_local location

local_directory = "C:/users/local_s2098893"
new_work_directory = "April_test_9"
new_directory_path = os.path.join(local_directory, new_work_directory)
new_directory_path = new_directory_path.replace("\\", "/")
print("New directory path:", new_directory_path)

if not os.path.exists(new_directory_path):
    os.mkdir(new_directory_path)
    print("Directory created at: " + new_directory_path)
else:
    print("Directory already exists: " + new_directory_path)

os.chdir(new_directory_path)
print("Changed working directory to: " + os.getcwd())

#Creating multiple folders
BaseDir = os.getcwd()
Foldername = 1

while os.path.exists(BaseDir+"/"+str(Foldername)) ==True:
    Foldername = Foldername + 1

os.mkdir(BaseDir+"/"+str(Foldername))
os.chdir(BaseDir+"/"+str(Foldername))

while os.path.exists(BaseDir+"/"+str(Foldername)) ==True:
    Foldername = Foldername + 1

os.mkdir(BaseDir+"/"+str(Foldername))
os.chdir(BaseDir+"/"+str(Foldername))

def CreateBeamModel(variables):
    
    top_flange_width = variables[0] #mm
    bottom_flange_width = variables[1] #mm
    web_height= variables[2] #mm
    top_flange_thickness = variables[3] #mm
    bottom_flange_thickness = variables[4] #mm
    web_thickness = variables[5] #mm
    span = variables[6] #mm
    mesh_size = variables[7]
    concentrated_force_beam = variables[8] #give downward loading as positive value
    number_of_runs = variables[9]
    yieldstrength = 355.0
    model_height = web_height + top_flange_thickness/2.0 + bottom_flange_thickness/2.0
    
    
    #Create new model
    Mdb()

    #This code creates the section through a sketch
    mdb.models['Model-1'].ConstrainedSketch(name='__profile__', sheetSize=200.0)
    mdb.models['Model-1'].sketches['__profile__'].Line(point1=(0.0, 0.0), point2=(
        bottom_flange_width/2.0, 0.0))
    mdb.models['Model-1'].sketches['__profile__'].HorizontalConstraint(
        addUndoState=False, entity=
        mdb.models['Model-1'].sketches['__profile__'].geometry[2])
    mdb.models['Model-1'].sketches['__profile__'].Line(point1=(0.0, 0.0), point2=(
        -bottom_flange_width/2.0, 0.0))
    mdb.models['Model-1'].sketches['__profile__'].HorizontalConstraint(
        addUndoState=False, entity=
        mdb.models['Model-1'].sketches['__profile__'].geometry[3])
    mdb.models['Model-1'].sketches['__profile__'].Line(point1=(0.0, model_height), point2=
        (0.0, 0.0))
    mdb.models['Model-1'].sketches['__profile__'].VerticalConstraint(addUndoState=
        False, entity=mdb.models['Model-1'].sketches['__profile__'].geometry[4])
    mdb.models['Model-1'].sketches['__profile__'].Line(point1=(-top_flange_width/2.0, model_height),
        point2=(0.0, model_height))
    mdb.models['Model-1'].sketches['__profile__'].HorizontalConstraint(
        addUndoState=False, entity=
        mdb.models['Model-1'].sketches['__profile__'].geometry[5])
    mdb.models['Model-1'].sketches['__profile__'].Line(point1=(0.0, model_height), point2=
        (top_flange_width/2.0, model_height))
    mdb.models['Model-1'].sketches['__profile__'].HorizontalConstraint(
        addUndoState=False, entity=
        mdb.models['Model-1'].sketches['__profile__'].geometry[6])
    mdb.models['Model-1'].Part(dimensionality=THREE_D, name='Part-1', type=
        DEFORMABLE_BODY)

    #Here we specify the depth (length) of the beam
    mdb.models['Model-1'].parts['Part-1'].BaseShellExtrude(depth=span, sketch=
        mdb.models['Model-1'].sketches['__profile__'])
    del mdb.models['Model-1'].sketches['__profile__']
    mdb.models['Model-1'].ConstrainedSketch(gridSpacing=300.18, name='__profile__', 
        sheetSize=12007.27, transform=
        mdb.models['Model-1'].parts['Part-1'].MakeSketchTransform(
        sketchPlane=mdb.models['Model-1'].parts['Part-1'].faces[1], 
        sketchPlaneSide=SIDE1, 
        sketchUpEdge=mdb.models['Model-1'].parts['Part-1'].edges[4], 
        sketchOrientation=RIGHT, origin=(0.0, 104.5, 3000.0)))
    mdb.models['Model-1'].parts['Part-1'].projectReferencesOntoSketch(filter=
        COPLANAR_EDGES, sketch=mdb.models['Model-1'].sketches['__profile__'])
     
    
    # SPECIFY COVER
    
    circle_radius = random.uniform(30.0,40.0)
    
    cover = circle_radius+10
    
    #LETS DEFINE SOME VARIBALES THAT WILL HELP US DRAW THE CIRCLES THAT WE WANT   
   
    
    height_origin_circle = web_height/2.0
   


    # lower_bound_y = 0.0+cover+circle_radius
    # upper_bound_y = web_height-cover-circle_radius
    
    # lower_bound_x = 0.0+cover+circle_radius
    # upper_bound_x = span - cover - circle_radius
    
    lower_bound_y = (web_height/2)-cover-20
    upper_bound_y = -(web_height/2)+cover+20
    
    lower_bound_x = -(span/2.0)+cover+20
    upper_bound_x = (span/2.0)-cover-20
    
    
    
    def generate_non_intersecting_holes(num_holes, radius, lower_bound_x, lower_bound_y, upper_bound_x, upper_bound_y):
        hole_centers = []
        max_attempts = 300000  # Limit to avoid infinite loops
        
        for _ in range(num_holes):  # For each hole to be generated
            attempts = 0
            while attempts < max_attempts:
                x = random.uniform(lower_bound_x, upper_bound_x)
                #y = random.uniform(lower_bound_y, upper_bound_y)
                y = (random.uniform(lower_bound_y, upper_bound_y))*-1.0
                candidate_center = (x, y)
                
                # Check that the candidate does not intersect existing holes and minimum seperation requirement
                if all(np.linalg.norm(np.array(candidate_center) - np.array(existing)) >= 2 * (radius + 20.0) for existing in hole_centers):
                    hole_centers.append(candidate_center)
                    break
                attempts += 1
            
            if attempts == max_attempts:
                raise ValueError("Could not generate non-intersecting holes within bounds.")
        
        return hole_centers
          
    hole_centers = generate_non_intersecting_holes(15, circle_radius, lower_bound_x, lower_bound_y, upper_bound_x, upper_bound_y)
     
    print(hole_centers)
    print("holes generated correctly") 
    
    """
    def save_hole_centers_to_csv(hole_centers, folder_path):
        csv_file_path = os.path.join(folder_path, 'hole_centers.csv')
        with open(csv_file_path, 'w') as file:  # Open the file for writing
            writer = csv.writer(file, lineterminator='\n')  # Added lineterminator='\n'
            writer.writerow(['x', 'y'])  # Writing the header
            for center in hole_centers:
                writer.writerow(center)  # Writing each (x, y) pair
        print("Hole centers saved to {}".format(csv_file_path))

    save_hole_centers_to_csv(hole_centers, NameFolder)
    """
    
    def save_hole_centers_to_csv(hole_centers, radius, folder_path):
        # Define the path for the CSV file
        csv_file_path = os.path.join(folder_path, 'hole_centers.csv')
        
        with open(csv_file_path, 'w') as file:  # Open the file for writing
            writer = csv.writer(file, lineterminator='\n')  # Using lineterminator='\n'
            
            # Write the header (x, y, radius)
            writer.writerow(['x', 'y', 'radius'])  # Adding 'radius' as the last column in the header
            
            # Write each (x, y) pair and the radius
            for center in hole_centers:
                writer.writerow(list(center) + [radius])  # Append the radius as the last entry
            
        print("Hole centers and radii saved to {}".format(csv_file_path))
    
    save_hole_centers_to_csv(hole_centers, circle_radius, NameFolder)
    
    #This section creates the material
    mdb.models['Model-1'].Material(name='Material-1')
    mdb.models['Model-1'].materials['Material-1'].Elastic(table=((210000.0, 0.3), 
        ))
    mdb.models['Model-1'].materials['Material-1'].Plastic(table=((yieldstrength, 0.0), ))

    #This creates the three sections with different thicknesses
    mdb.models['Model-1'].HomogeneousShellSection(idealization=NO_IDEALIZATION, 
        integrationRule=SIMPSON, material='Material-1', name='Section-1', 
        nodalThicknessField='', numIntPts=5, poissonDefinition=DEFAULT, 
        preIntegrate=OFF, temperature=GRADIENT, thickness=top_flange_thickness, thicknessField='',
        thicknessModulus=None, thicknessType=UNIFORM, useDensity=OFF)
    mdb.models['Model-1'].HomogeneousShellSection(idealization=NO_IDEALIZATION, 
        integrationRule=SIMPSON, material='Material-1', name='Section-2', 
        nodalThicknessField='', numIntPts=5, poissonDefinition=DEFAULT, 
        preIntegrate=OFF, temperature=GRADIENT, thickness=web_thickness, thicknessField='',
        thicknessModulus=None, thicknessType=UNIFORM, useDensity=OFF)
    mdb.models['Model-1'].HomogeneousShellSection(idealization=NO_IDEALIZATION, 
        integrationRule=SIMPSON, material='Material-1', name='Section-3', 
        nodalThicknessField='', numIntPts=5, poissonDefinition=DEFAULT, 
        preIntegrate=OFF, temperature=GRADIENT, thickness=bottom_flange_thickness, thicknessField='',
        thicknessModulus=None, thicknessType=UNIFORM, useDensity=OFF)
        
        
        
        
    #This assignes the sections to each plate
    #This was done in the following order: top flange, web, bottom flange    
        
    mdb.models['Model-1'].parts['Part-1'].Set(faces=
        mdb.models['Model-1'].parts['Part-1'].faces.getSequenceFromMask(('[#3 ]', 
        ), ), name='Set-1')
    mdb.models['Model-1'].parts['Part-1'].SectionAssignment(offset=0.0, 
        offsetField='', offsetType=MIDDLE_SURFACE, region=
        mdb.models['Model-1'].parts['Part-1'].sets['Set-1'], sectionName=
        'Section-1', thicknessAssignment=FROM_SECTION)
   
    mdb.models['Model-1'].parts['Part-1'].Set(faces=
        mdb.models['Model-1'].parts['Part-1'].faces.getSequenceFromMask(('[#10 ]', 
        ), ), name='Set-2')
    mdb.models['Model-1'].parts['Part-1'].SectionAssignment(offset=0.0, 
        offsetField='', offsetType=MIDDLE_SURFACE, region=
        mdb.models['Model-1'].parts['Part-1'].sets['Set-2'], sectionName=
        'Section-2', thicknessAssignment=FROM_SECTION)
   
    mdb.models['Model-1'].parts['Part-1'].Set(faces=
        mdb.models['Model-1'].parts['Part-1'].faces.getSequenceFromMask(('[#c ]', 
        ), ), name='Set-3')
    mdb.models['Model-1'].parts['Part-1'].SectionAssignment(offset=0.0, 
        offsetField='', offsetType=MIDDLE_SURFACE, region=
        mdb.models['Model-1'].parts['Part-1'].sets['Set-3'], sectionName=
        'Section-3', thicknessAssignment=FROM_SECTION)

    #Here we create the assembly
    mdb.models['Model-1'].rootAssembly.DatumCsysByDefault(CARTESIAN)
    mdb.models['Model-1'].rootAssembly.Instance(dependent=ON, name='Part-1-1', 
        part=mdb.models['Model-1'].parts['Part-1'])

    #Here we create the step (Static step)
    #mdb.models['Model-1'].StaticStep(name='Step-1', previous='Initial')
    
    #Here we create the step (incremental step)
    mdb.models['Model-1'].StaticStep(initialInc=0.01, maxInc=0.01, name='Step-1', nlgeom=ON, previous='Initial')

    #To create the point at midspan, the instance had to be made independent
    mdb.models['Model-1'].rootAssembly.makeIndependent(instances=(
        mdb.models['Model-1'].rootAssembly.instances['Part-1-1'], ))


        
      


    
    #CUT-EXTRUCDE
    mdb.models['Model-1'].ConstrainedSketch(name='__profile__', sheetSize=200.0)
    mdb.models['Model-1'].sketches['__profile__'].Line(point1=(0.0, 0.0), point2=(
        100.0, 0.0))
    mdb.models['Model-1'].sketches['__profile__'].HorizontalConstraint(
        addUndoState=False, entity=
        mdb.models['Model-1'].sketches['__profile__'].geometry[2])
    mdb.models['Model-1'].sketches['__profile__'].Line(point1=(0.0, 0.0), point2=(
        -100.0, 0.0))
    mdb.models['Model-1'].sketches['__profile__'].HorizontalConstraint(
        addUndoState=False, entity=
        mdb.models['Model-1'].sketches['__profile__'].geometry[3])
    mdb.models['Model-1'].sketches['__profile__'].Line(point1=(0.0, 270.0), point2=
        (0.0, 0.0))
    mdb.models['Model-1'].sketches['__profile__'].VerticalConstraint(addUndoState=
        False, entity=mdb.models['Model-1'].sketches['__profile__'].geometry[4])
    mdb.models['Model-1'].sketches['__profile__'].Line(point1=(-90.0, 270.0), 
        point2=(0.0, 270.0))
    mdb.models['Model-1'].sketches['__profile__'].HorizontalConstraint(
        addUndoState=False, entity=
        mdb.models['Model-1'].sketches['__profile__'].geometry[5])
    mdb.models['Model-1'].sketches['__profile__'].Line(point1=(0.0, 270.0), point2=
        (90.0, 270.0))
    mdb.models['Model-1'].sketches['__profile__'].HorizontalConstraint(
        addUndoState=False, entity=
        mdb.models['Model-1'].sketches['__profile__'].geometry[6])
    mdb.models['Model-1'].Part(dimensionality=THREE_D, name='Part-1', type=
        DEFORMABLE_BODY)
    mdb.models['Model-1'].parts['Part-1'].BaseShellExtrude(depth=3000, sketch=
        mdb.models['Model-1'].sketches['__profile__'])
    del mdb.models['Model-1'].sketches['__profile__']
    mdb.models['Model-1'].ConstrainedSketch(gridSpacing=300.18, name='__profile__', 
        sheetSize=12007.27, transform=
        mdb.models['Model-1'].parts['Part-1'].MakeSketchTransform(
        sketchPlane=mdb.models['Model-1'].parts['Part-1'].faces[1], 
        sketchPlaneSide=SIDE1, 
        sketchUpEdge=mdb.models['Model-1'].parts['Part-1'].edges[4], 
        sketchOrientation=RIGHT, origin=(0.0, 104.5, 3000.0)))
    mdb.models['Model-1'].parts['Part-1'].projectReferencesOntoSketch(filter=
        COPLANAR_EDGES, sketch=mdb.models['Model-1'].sketches['__profile__'])
    mdb.models['Model-1'].Material(name='Material-1')
    mdb.models['Model-1'].materials['Material-1'].Elastic(table=((210000.0, 0.3), 
        ))
    mdb.models['Model-1'].materials['Material-1'].Plastic(table=((355.0, 0.0), ))
    mdb.models['Model-1'].HomogeneousShellSection(idealization=NO_IDEALIZATION, 
        integrationRule=SIMPSON, material='Material-1', name='Section-1', 
        nodalThicknessField='', numIntPts=5, poissonDefinition=DEFAULT, 
        preIntegrate=OFF, temperature=GRADIENT, thickness=20, thicknessField='', 
        thicknessModulus=None, thicknessType=UNIFORM, useDensity=OFF)
    mdb.models['Model-1'].HomogeneousShellSection(idealization=NO_IDEALIZATION, 
        integrationRule=SIMPSON, material='Material-1', name='Section-2', 
        nodalThicknessField='', numIntPts=5, poissonDefinition=DEFAULT, 
        preIntegrate=OFF, temperature=GRADIENT, thickness=20, thicknessField='', 
        thicknessModulus=None, thicknessType=UNIFORM, useDensity=OFF)
    mdb.models['Model-1'].HomogeneousShellSection(idealization=NO_IDEALIZATION, 
        integrationRule=SIMPSON, material='Material-1', name='Section-3', 
        nodalThicknessField='', numIntPts=5, poissonDefinition=DEFAULT, 
        preIntegrate=OFF, temperature=GRADIENT, thickness=20, thicknessField='', 
        thicknessModulus=None, thicknessType=UNIFORM, useDensity=OFF)
    mdb.models['Model-1'].parts['Part-1'].Set(faces=
        mdb.models['Model-1'].parts['Part-1'].faces.getSequenceFromMask(('[#12 ]', 
        ), ), name='Set-1')
    mdb.models['Model-1'].parts['Part-1'].SectionAssignment(offset=0.0, 
        offsetField='', offsetType=MIDDLE_SURFACE, region=
        mdb.models['Model-1'].parts['Part-1'].sets['Set-1'], sectionName=
        'Section-1', thicknessAssignment=FROM_SECTION)
    mdb.models['Model-1'].parts['Part-1'].Set(faces=
        mdb.models['Model-1'].parts['Part-1'].faces.getSequenceFromMask(('[#1 ]', 
        ), ), name='Set-2')
    mdb.models['Model-1'].parts['Part-1'].SectionAssignment(offset=0.0, 
        offsetField='', offsetType=MIDDLE_SURFACE, region=
        mdb.models['Model-1'].parts['Part-1'].sets['Set-2'], sectionName=
        'Section-2', thicknessAssignment=FROM_SECTION)
    mdb.models['Model-1'].parts['Part-1'].Set(faces=
        mdb.models['Model-1'].parts['Part-1'].faces.getSequenceFromMask(('[#c ]', 
        ), ), name='Set-3')
    mdb.models['Model-1'].parts['Part-1'].SectionAssignment(offset=0.0, 
        offsetField='', offsetType=MIDDLE_SURFACE, region=
        mdb.models['Model-1'].parts['Part-1'].sets['Set-3'], sectionName=
        'Section-3', thicknessAssignment=FROM_SECTION)
    mdb.models['Model-1'].rootAssembly.DatumCsysByDefault(CARTESIAN)
    mdb.models['Model-1'].rootAssembly.Instance(dependent=ON, name='Part-1-1', 
        part=mdb.models['Model-1'].parts['Part-1'])
    mdb.models['Model-1'].StaticStep(initialInc=0.01, maxInc=0.01, name='Step-1', 
        nlgeom=ON, previous='Initial')
    mdb.models['Model-1'].rootAssembly.makeIndependent(instances=(
        mdb.models['Model-1'].rootAssembly.instances['Part-1-1'], ))
    # mdb.models['Model-1'].rootAssembly.PartitionEdgeByParam(edges=
        # mdb.models['Model-1'].rootAssembly.instances['Part-1-1'].edges.getSequenceFromMask(
        # ('[#40 ]', ), ), parameter=0.5)
    # mdb.models['Model-1'].rootAssembly.Set(name='Set-4', vertices=
        # mdb.models['Model-1'].rootAssembly.instances['Part-1-1'].vertices.getSequenceFromMask(
        # ('[#80 ]', ), ))
    # mdb.models['Model-1'].ConcentratedForce(cf2=-5000, createStepName='Step-1', 
        # distributionType=UNIFORM, field='', localCsys=None, name='Load-1', region=
        # mdb.models['Model-1'].rootAssembly.sets['Set-4'])
        
        
        
        
    #testing load here
    # del mdb.models['Model-1'].loads['Load-1']
    # mdb.models['Model-1'].loads['Load-1']

        
    #create boundary conditions    
    mdb.models['Model-1'].DisplacementBC(amplitude=UNSET, createStepName='Step-1', 
        distributionType=UNIFORM, fieldName='', fixed=OFF, localCsys=None, name=
        'BC-1', region=Region(
        edges=mdb.models['Model-1'].rootAssembly.instances['Part-1-1'].edges.getSequenceFromMask(
        mask=('[#900 ]', ), )), u1=0.0, u2=0.0, u3=0.0, ur1=UNSET, ur2=UNSET, ur3=
        UNSET)
    mdb.models['Model-1'].DisplacementBC(amplitude=UNSET, createStepName='Step-1', 
        distributionType=UNIFORM, fieldName='', fixed=OFF, localCsys=None, name=
        'BC-2', region=Region(
        edges=mdb.models['Model-1'].rootAssembly.instances['Part-1-1'].edges.getSequenceFromMask(
        mask=('[#1400 ]', ), )), u1=0.0, u2=0.0, u3=UNSET, ur1=UNSET, ur2=UNSET, 
        ur3=UNSET)
        
        
    mdb.models['Model-1'].sketches.changeKey(fromName='__profile__', toName=
        '__save__')
    mdb.models['Model-1'].ConstrainedSketch(gridSpacing=150.6, name='__profile__', 
        sheetSize=6024.25, transform=
        mdb.models['Model-1'].parts['Part-1'].MakeSketchTransform(
        sketchPlane=mdb.models['Model-1'].parts['Part-1'].faces[1], 
        sketchPlaneSide=SIDE1, 
        sketchUpEdge=mdb.models['Model-1'].parts['Part-1'].edges[4], 
        sketchOrientation=RIGHT, origin=(0.0, 135.0, 1500.0)))
    mdb.models['Model-1'].parts['Part-1'].projectReferencesOntoSketch(filter=
        COPLANAR_EDGES, sketch=mdb.models['Model-1'].sketches['__profile__'])
    mdb.models['Model-1'].sketches['__profile__'].retrieveSketch(sketch=
        mdb.models['Model-1'].sketches['__save__'])
    del mdb.models['Model-1'].sketches['__save__']
    



        
        

    del mdb.models['Model-1'].sketches['__profile__']
    mdb.models['Model-1'].ConstrainedSketch(gridSpacing=150.6, name='__profile__', 
        sheetSize=6024.25, transform=
        mdb.models['Model-1'].parts['Part-1'].MakeSketchTransform(
        sketchPlane=mdb.models['Model-1'].parts['Part-1'].faces[1], 
        sketchPlaneSide=SIDE1, 
        sketchUpEdge=mdb.models['Model-1'].parts['Part-1'].edges[4], 
        sketchOrientation=RIGHT, origin=(0.0, 135.0, 1500.0)))
    mdb.models['Model-1'].parts['Part-1'].projectReferencesOntoSketch(filter=
        COPLANAR_EDGES, sketch=mdb.models['Model-1'].sketches['__profile__'])
        

    for center in hole_centers:  # Loop through each (x, y) tuple in the list
        x, y = center  # Unpack the tuple
        #print(x, y)  # Print the center coordinates
        mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(
            center=(x, y), 
        point1=(x + circle_radius, y - circle_radius)  # Adjust `point1` logic as needed
    )
    
    # for center in hole_centers:  # Loop through each (x, y) tuple in the list
        # x, y = center  # Unpack the tuple
        # mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(
            # center=(x, y), 
            # point1=(x + circle_radius, y - circle_radius)  # Adjust `point1` logic as needed
            # print(x, y)
        # )

    for temp in range (0, len(hole_centers)):

        mdb.models['Model-1'].sketches['__profile__'].RadialDimension(curve=
            mdb.models['Model-1'].sketches['__profile__'].geometry[temp+10], radius=circle_radius, 
            textPoint=(-1500, -0))
    
        
    # mdb.models['Model-1'].sketches['__profile__'].RadialDimension(curve=
        # mdb.models['Model-1'].sketches['__profile__'].geometry[10], radius=circle_radius, 
        # textPoint=(-1092.97143554688, -288.601623535156))
    # mdb.models['Model-1'].sketches['__profile__'].RadialDimension(curve=
        # mdb.models['Model-1'].sketches['__profile__'].geometry[11], radius=circle_radius, 
        # textPoint=(-450.266845703125, -292.301635742188))
    # mdb.models['Model-1'].sketches['__profile__'].RadialDimension(curve=
        # mdb.models['Model-1'].sketches['__profile__'].geometry[12], radius=circle_radius, 
        # textPoint=(147.598022460938, -284.901550292969))
    mdb.models['Model-1'].parts['Part-1'].CutExtrude(flipExtrudeDirection=OFF, 
        sketch=mdb.models['Model-1'].sketches['__profile__'], sketchOrientation=
        RIGHT, sketchPlane=mdb.models['Model-1'].parts['Part-1'].faces[1], 
        sketchPlaneSide=SIDE1, sketchUpEdge=
        mdb.models['Model-1'].parts['Part-1'].edges[4])
    del mdb.models['Model-1'].sketches['__profile__']
    
    
    
    mdb.models['Model-1'].rootAssembly.regenerate()
    
    # mdb.models['Model-1'].rootAssembly.PartitionEdgeByParam(edges=
        # mdb.models['Model-1'].rootAssembly.instances['Part-1-1'].edges.getSequenceFromMask(
        # ('[#80000 ]', ), ), parameter=0.5)
    # mdb.models['Model-1'].rootAssembly.Set(name='Set-5', vertices=
        # mdb.models['Model-1'].rootAssembly.instances['Part-1-1'].vertices.getSequenceFromMask(
        # ('[#100000 ]', ), ))
    # mdb.models['Model-1'].ConcentratedForce(cf2=-5000.0, createStepName='Step-1', 
        # distributionType=UNIFORM, field='', localCsys=None, name='Load-1', region=
        # mdb.models['Model-1'].rootAssembly.sets['Set-5'])

    #DELETE QUOTATIONS 
#test load
    mdb.models['Model-1'].rootAssembly.deleteMesh(regions=
        mdb.models['Model-1'].rootAssembly.instances['Part-1-1'].faces.getSequenceFromMask(
        ('[#13 ]', ), ))
    mdb.models['Model-1'].rootAssembly.PartitionEdgeByParam(edges=
        mdb.models['Model-1'].rootAssembly.instances['Part-1-1'].edges.getSequenceFromMask(
        ('[#40000 ]', ), ), parameter=0.5)
    mdb.models['Model-1'].rootAssembly.Set(name='Set-4', vertices=
        mdb.models['Model-1'].rootAssembly.instances['Part-1-1'].vertices.getSequenceFromMask(
        ('[#80000 ]', ), ))
    mdb.models['Model-1'].ConcentratedForce(cf2=-concentrated_force_beam, createStepName='Step-1', 
        distributionType=UNIFORM, field='', localCsys=None, name='Load-2', region=
        mdb.models['Model-1'].rootAssembly.sets['Set-4'])  



    #TEST boundary conditions
    del mdb.models['Model-1'].boundaryConditions['BC-1']
    del mdb.models['Model-1'].boundaryConditions['BC-2']
    mdb.models['Model-1'].rootAssembly.Set(edges=
        mdb.models['Model-1'].rootAssembly.instances['Part-1-1'].edges.getSequenceFromMask(
        ('[#4800000 ]', ), ), name='Set-6')
    mdb.models['Model-1'].DisplacementBC(amplitude=UNSET, createStepName='Step-1', 
        distributionType=UNIFORM, fieldName='', fixed=OFF, localCsys=None, name=
        'BC-1', region=mdb.models['Model-1'].rootAssembly.sets['Set-6'], u1=0.0, 
        u2=0.0, u3=0.0, ur1=UNSET, ur2=UNSET, ur3=UNSET)
    mdb.models['Model-1'].rootAssembly.Set(edges=
        mdb.models['Model-1'].rootAssembly.instances['Part-1-1'].edges.getSequenceFromMask(
        ('[#a000000 ]', ), ), name='Set-7')
    mdb.models['Model-1'].DisplacementBC(amplitude=UNSET, createStepName='Step-1', 
        distributionType=UNIFORM, fieldName='', fixed=OFF, localCsys=None, name=
        'BC-2', region=mdb.models['Model-1'].rootAssembly.sets['Set-7'], u1=0.0, 
        u2=0.0, u3=UNSET, ur1=UNSET, ur2=UNSET, ur3=UNSET)


    #This meshes the assembly
    mdb.models['Model-1'].rootAssembly.seedPartInstance(deviationFactor=0.1, 
        minSizeFactor=0.1, regions=(
        mdb.models['Model-1'].rootAssembly.instances['Part-1-1'], ), size=mesh_size)
    mdb.models['Model-1'].rootAssembly.generateMesh(regions=(
        mdb.models['Model-1'].rootAssembly.instances['Part-1-1'], ))



    #DELETE QUOTATIONS 
    
    #This creates the job
    mdb.Job(atTime=None, contactPrint=OFF, description='', echoPrint=OFF, 
        explicitPrecision=SINGLE, getMemoryFromAnalysis=True, historyPrint=OFF, 
        memory=90, memoryUnits=PERCENTAGE, model='Model-1', modelPrint=OFF, 
        multiprocessingMode=DEFAULT, name='Job-1', nodalOutputPrecision=SINGLE, 
        numCpus=1, numGPUs=0, queue=None, resultsFormat=ODB, scratch='', type=
        ANALYSIS, userSubroutine='', waitHours=0, waitMinutes=0)
    

    #This submits the job
    mdb.jobs['Job-1'].submit(consistencyChecking=OFF)

    #This waits for the job to complete
    mdb.jobs['Job-1'].waitForCompletion()
    
      

       


    

     
 
    
    
#DELETE QUOTATIONS 

def PostProcessing():
    CurrentDir=os.getcwd()
    odb = session.openOdb(CurrentDir + '/Job-1.odb')
    NrOfSteps=len(odb.steps['Step-1'].frames)
   
    Displacements = []
 
    for i in range(NrOfSteps):
        central_disp=odb.steps['Step-1'].frames[i].fieldOutputs['U'].values[2].data[1]*-1
        Displacements.append(central_disp)
        
    Forces = []
    for i in range(NrOfSteps):
        applied_force=odb.steps['Step-1'].frames[i].fieldOutputs['CF'].values[2].data[1]*-1
        Forces.append(applied_force)

    fig, ax = plt.subplots()
    ax.plot(Displacements, Forces, color='r', label='U2')
    plt.legend()
    ax.set(xlabel='Displacements [mm]', ylabel='Applied Load [kN]', title='Force Displacement Curve')
    ax.grid()
    fig.savefig("MAX_DISPLACEMENT.png")
    plt.close(fig)



models = []
for top_flange_width in [180.0]:
    for bottom_flange_width in [200.0]:
        for web_height in [250]:
            for top_flange_thickness in [20]:
                for bottom_flange_thickness in [20]:
                    for web_thickness in [20]:
                        for span in [3000]:
                            for mesh_size in [30]:
                                #for concentrated_force_beam in np.arange(5000.0, 20001.0, 5000):
                                for concentrated_force_beam in [50000]:
                                    for number_of_runs in np.arange(51, 60.1, 1):
                                    #first_nr = first number of file, last number = last number of file
                                        models.append([top_flange_width, bottom_flange_width, web_height, top_flange_thickness, bottom_flange_thickness, web_thickness, span, mesh_size, concentrated_force_beam, number_of_runs])
                                    
print(models)


"""
def extract_field_output_to_csv(odb_file_path, output_variable, folder_path, file_name='field_output.csv'):
    # Open the ODB file
    odb = openOdb(odb_file_path)
    
    # Access the step and frame from which we want to extract field outputs
    step = odb.steps['Step-1']  # Change this if you want a different step
    frame = step.frames[-1]  # Last frame

    # Extract the field output (e.g., 'U' for displacement, 'S' for stress)
    field_output = frame.fieldOutputs[output_variable]
    
    # Prepare to store data
    node_data = []
    
    # Loop over all values (nodes or elements) and extract the required data
    for value in field_output.values:
        node_label = value.nodeLabel
        node_value = value.data  # This is the field output data, e.g., displacement values
        
        # Check if the output variable is 'U' (displacement) and split the components (U1, U2, U3)
        if output_variable == 'U':  # Displacement field (U1, U2, U3)
            node_data.append([node_label] + list(node_value))  # Add the node label and displacement components
        else:
            node_data.append([node_label] + [node_value])  # For other variables, just add them in one column

    # Define the path for the CSV file
    csv_file_path = os.path.join(folder_path, file_name)
    
    # Write the data to the CSV file
    with open(csv_file_path, 'w') as file:
        writer = csv.writer(file, lineterminator='\n')  # Using lineterminator='\n' for correct line breaks
        
        # Write the header (node label and field variable components)
        if output_variable == 'U':  # If the output is displacement, list the components U1, U2, U3
            header = ['Node Label', 'U1', 'U2', 'U3']
        else:
            header = ['Node Label', output_variable]  # For other output variables like 'S', 'RF', etc.
        writer.writerow(header)
        
        # Write the data
        for data in node_data:
            writer.writerow(data)
    
    # Print the path where the output was saved
    print("Field output saved to {}".format(csv_file_path))
"""

def extract_field_output_to_csv(odb_file_path, output_variable, folder_path, file_name='field_output.csv'):
    # Open the ODB file
    odb = openOdb(odb_file_path)
    
    # Access the step and frame from which we want to extract field outputs
    step = odb.steps['Step-1']  # Change this if you want a different step
    frame = step.frames[-1]  # Last frame

    # Extract the field output (e.g., 'U' for displacement, 'S' for stress)
    field_output = frame.fieldOutputs[output_variable]
    
    # Access the instance to get the node set and coordinates
    instance = odb.rootAssembly.instances[list(odb.rootAssembly.instances.keys())[0]]  # Assuming a single instance
    nodes = instance.nodes  # All nodes in the instance

    # Create a dictionary mapping node labels to coordinates for quick lookup
    node_coordinates = {node.label: node.coordinates for node in nodes}

    # Prepare to store data
    node_data = []
    
    # Loop over all values (nodes or elements) and extract the required data
    for value in field_output.values:
        node_label = value.nodeLabel
        node_value = value.data  # This is the field output data, e.g., displacement values
        coordinates = node_coordinates[node_label]  # Retrieve the coordinates (x, y, z)
        
        # Check if the output variable is 'U' (displacement) and split the components (U1, U2, U3)
        if output_variable == 'U':  # Displacement field (U1, U2, U3)
            node_data.append([node_label] + list(coordinates) + list(node_value))  # Add the node label, coordinates, and displacement components
        else:
            node_data.append([node_label] + list(coordinates) + [node_value])  # For other variables, add coordinates and the value

    # Define the path for the CSV file
    csv_file_path = os.path.join(folder_path, file_name)
    
    # Write the data to the CSV file
    with open(csv_file_path, 'w') as file:
        writer = csv.writer(file, lineterminator='\n')  # Using lineterminator='\n' for correct line breaks
        
        # Write the header (node label, coordinates, and field variable components)
        if output_variable == 'U':  # If the output is displacement, list the components U1, U2, U3
            header = ['Node Label', 'X', 'Y', 'Z', 'U1', 'U2', 'U3']
        else:
            header = ['Node Label', 'X', 'Y', 'Z', output_variable]  # For other output variables like 'S', 'RF', etc.
        writer.writerow(header)
        
        # Write the data
        for data in node_data:
            writer.writerow(data)
    
    # Print the path where the output was saved
    print("Field output saved to {}".format(csv_file_path))    
    

    
    








#creating folder with parameter names
counter = 1
for i in models:
    
    ModelName = str(i[0])
    for j in i[1:]:
        ModelName = ModelName + "_" + str(j)
    NameFolder= BaseDir + "/" + str(Foldername) + "/" + ModelName
    # print(NameFolder)
    os.mkdir(NameFolder)
    os.chdir(NameFolder)
    CreateBeamModel(i)
    odb_file_path = os.path.join(NameFolder, 'Job-1.odb')
    ###testesttest
    if os.path.exists(odb_file_path):
        # Extract field output (e.g., 'U' for displacements) and save to CSV
        output_variable = 'U'  # Change to 'S' for stresses, 'RF' for reaction forces, etc.
        extract_field_output_to_csv(odb_file_path, output_variable, NameFolder, file_name='field_output.csv')
    else:
        print("Warning: ODB file not found for model: {}".format(ModelName))
    #endendendtest
    PostProcessing()
    #save_hole_centers_to_csv(hole_centers, NameFolder)
    print("------------------------------MODEL "+ str(counter) +" FINISHED------------------------------")
    counter = counter +1






destination = r"C:/Users/s2098893/OneDrive - University of Edinburgh/data_generation batch 0-350"

# Check the number of folders in the directory

def count_folders_in_directory(directory):
    source = new_directory_path
    #destination = r"C:/Users/s2098893/OneDrive - University of Edinburgh/output_test_2"
    folder_count = 0
    for item in os.listdir(directory):
        item_path = os.path.join(directory, item)
        if os.path.isdir(item_path):
            folder_count += 1
    return folder_count

# Check the number of folders in the directory once
if os.path.exists(new_directory_path):
    num_folders = count_folders_in_directory(new_directory_path)
    print("Number of folders in '{}' is: {}".format(new_directory_path, num_folders))
    
    if num_folders == 2:  # Check if the number of folders is equal to 100
        if os.path.exists(destination):
            shutil.rmtree(destination)  # Remove destination if it already exists
        
        shutil.copytree(new_directory_path, destination)
        print("Directory copied to: " + destination)
        print("Files and folders have been copied to the destination.")
    else:
        print("The directory contains {} folders, not 100.".format(num_folders))
else:
    print("The specified directory does not exist: " + new_directory_path)


#Checking the time it took to run the simulations

print("run complete")
end_time = time.time()
elapsed_time = end_time - start_time
print("Total execution time: {:.2f} seconds".format(elapsed_time))