---
title: Research
layout: default

---
{::options parse_block_html="true" /}

## Data Collection


<!-- <div style="float:right; margin:1em">
<img src="{{ site.url }}img/raingage.jpg" width=250px height=250px alt="Wireless raingage">
</div> -->

<div style="float:right; margin:1em">
![raingage]({{site.baseurl}}/img/raingage.jpg){:height="250px" width="250px"}
</div>

Data collection is an essential component of Water Resources modeling. Watershed studies in Columbia, SC often use data collected by state and federal institutions to drive their simulations. Unfortunately, this data lacks sufficient spatial and temporal resolution to accurately simulate hydro-environmental watershed processes. High resolution data, such as NEXRAD precipitation, has been found to be inaccurate due to the convective storms that dominate the region and produce spatially diverse rainfall patterns.  To overcome the lack of sufficient observation data, a network of clustered observation sensors will be deployed.

Research in underway to determine how a network of portable observation sensors can be deployed to monitor the city in and efficient and cost effective manner.  Given these goals, a prototype rain gage was recently developed from cheap electronic components that eliminates the need for an expensive data logger to store observation measurements. This new system is designed to wirelessly transmit data measurements to a server via REST web service communication.  Using this approach, portable sensors can be rapidly deployed and send their observations to a single data store.  

## Model Storage and Visualization on the Cloud
<div style="float: right; margin: 1em">
![cloud]({{site.baseurl}}/img/swat_hosting.jpg){:height="274px" width="400px"}
<!-- <img src="{{ site.url }}img/swat_hosting.jpg" width=400px height=275px alt="SWAT model hosting and visualization."> -->
</div>


This research endeavor seeks to evaluate the viability of cloud hosting solutions for Water Resources modeling.  The Microsoft Azure cloud computing platform enables developers to create web applications that utilize the storage, redundancy, and compute power of the Azure grid. The primary advantage of this resource is its relatively low learning curve which allows scientists to rapidly prototype web applications. 

The goal of this research is to investigate how the Microsoft Azure computing environment can be used to store and visualize water resources models.  To evaluate this capacity, a web application is under development to host Soil and Water Assessment Tool (SWAT) simulations, <a target="_blank" href="http://swathosting.cloudapp.net">SWAT Portal</a>.  While this project is still in its infancy, it is currently capable of storing and retrieving model simulations, results visualization, and data editing. Work is underway to make this application a full hosting environment for SWAT simulations, including model preparation and simulation.  

<br>

## Large Scale Watershed Delineation

<div style="float: right; margin: 1em">
![watershed]({{site.baseurl}}/img/watershed.jpg){:height="255px" width="380px"}	
<!-- <img src="{{ site.url }}img/watershed.jpg" width=380px height=255px alt="Watershed delineation using a hierarchical approach"> -->
</div>

Most water resources applications required data processing routines which can be performed on a standard desktop computer, using open source or commercially licensed software. However, large scale applications are significantly more computationally demanding. For these large watersheds, standard GIS software does not perform favorably because algorithms are typically optimized for CPU efficiency, rather than data input and output (Arge et al., 2003). Within the scientific community, software systems have been designed to overcome this shortcoming by utilizing High Performance Computing (HPC) or High Throughput Computing (HTC) techniques (e.g. Gong and Xie 2009; Wallis et al. 2010). To implement these methods, users must have experience with, and have access to advanced computing environments. While these approaches are capable of significant computational speedup, the additional complexity of these solutions also deters users (Mineter et al., 2000). 

This area of my research focuses on how pre-processed <a target="_blank" href="http://www.horizon-systems.com/NHDPlus/NHDPlusV2_data.php">NHD+</a> data can be leveraged to rapidly reconstruct watershed boundaries from pre-computed catchment geometries. The major benefit of this approach is that it eliminates the redundant raster computations associated with watershed delineation. This work extends the method proposed by Djokic and Ye (2000) to create a watershed delineation tool that utilizes only pre-existing watershed data and is built from open source software. This work uses modern programming techniques and mathematical graph theory to form relationships between pre-processed watershed boundaries as well as relationships between cells of a flow direction grid. Using graphing algorithms, upstream flow direction cells and ultimately catchment boundaries are identified for a given outlet location. While this work is still underway, early results have shown that this delineation technique is substantially faster than currently used algorithms. 

<br>

## Service Oriented Modeling
<div style="float: right; margin: 1em">
![soa]({{site.baseurl}}/img/soa.jpg){:height="275px" width="400px"}
<!-- <img src="{{ site.url }}img/soa.jpg" width=400px height=275px alt="Streamflow results using service oriented models "> -->
</div>

Environmental modeling often requires the use of multiple data sources, models, and analysis routines coupled into a workflow to answer a research question. Coupling these computational resources can be accomplished using various tools, each requiring the developer to follow a specific protocol to ensure that components are linkable. Despite these coupling tools, it is not always straight forward to create a modeling workflow due to platform dependencies, computer architecture requirements, and programming language incompatibilities. A service-oriented approach that enables individual models to operate and interact with others using web services is one method for overcoming these challenges. 

This work advanced the idea of service-oriented modeling by presenting a design for a modeling service that builds from the <a target="_blank" href="http://www.opengeospatial.org/standards/wps">Open Geospatial Consortium (OGC) Web Processing Service (WPS)</a> protocol. This work demonstrated how the WPS protocol could be used to create modeling services, and then demonstrated how these modeling services can be brought into workflow environments using generic client-side code. This work was implemented within the <a href="#hydromodeler">HydroModeler</a> environment, a model coupling tool built on the Open Modeling Interface standard (version 1.4).


This work showed how a hydrology model can be hosted as a WPS web service and used within a client-side workflow. The primary advantage of this approach is that the server-side software follows an established standard that can be leveraged and reused within multiple workflow environments and decision support systems.  The findings of this study are published in **Castronova, et al. 2013**.

<br>


## HydroModeler
<a name="hydromodeler"></a>
<div style="float: right; margin: 1em">
![HM]({{site.baseurl}}/img/HM.jpg){:height="350px" width="500px"}
<!-- <img src="{{ site.url }}img/HM.jpeg" width=500px height=350px alt="The HydroModeler pluging for HydroDesktop"> -->
</div>

HydroModeler is a HydroDesktop plugin that extends its capabilities to include component-based model development. It is based on an open-source model editor provided by the OpenMI Association Technical Committee (OATC) Configuration Editor version 1.4 (<a target="_blank" href="http://www.openmi.org">OpenMI</a>). Its integration within the HydroDesktop environment provides the ability to both retrieve data from remote sources and to utilize this data in a model simulation. 

The goal of this work provide interoperability between the Consortium of Universities for the Advancement of Hydrologic Science, Inc. (CUAHSI) Hydrologic Information System (<a target="_blank" href="http://his.cuahsi.org">HIS</a>) and the Open Modeling Interface (OpenMI). The primary motivation for making these two systems interoperable is that the CUAHSI HIS has a primary focus on hydrologic data management and visualization while the OpenMI has a primary focus on integrated environmental modeling. By combining the two systems into a single software application, it is possible to create an integrated environmental modeling environment that scientists and engineers can use to understand and manage environmental systems. 

The findings from this study are published in **Castronova et al., 2013**.  This paper describes the design and implementation of this prototype software system, and presents an example application in which evapotranspiration is modeled using OpenMI components that consume HIS time series data for input. 

<br>

## Performance of Loosely Integrated Modeling

<div style="float: right; margin: 1em">
![hms]({{site.baseurl}}/img/smw_hms.jpg){:height="300px" width="300px"}
<!-- <img src="{{ site.url }}img/smw_hms.jpg" width=300px height=300px alt="OpenMI performance gains HEC-HMS"> -->
</div>

Due to the complex nature of watershed systems, it is often necessary to integrate multiple simulation models to predict holistic system response. This research explores the use of a component-based approach for the runtime integration of models, implemented as "plug-and-play" software components. Our motivation was to quantify performance overhead costs introduced by adopting a component-based paradigm for loosely integrating hydrologic simulation models. 

This research consisted of constructing a standard rainfall/runoff watershed system using the Open Modeling Interface (OpenMI) in which infiltration, surface runoff, and channel routing processes are each implemented as independent model components. The performance of this model was analyzed to quantify the computational scaling of the loose integration approach, against the Hydrologic Engineering Center's Hydrologic Modeling System (<a target="_blank" href="http://www.hec.usace.army.mil/software/hec-hms/">HMS</a>). The findings of this study are published in **Castronova and Goodall, 2013**. The results suggest that the overhead introduced by runtime communication of data is not significant when applied for semi-distributed watershed modeling. 

<br>

## The Simple Model Wrapper

Component software architectures offer an alternative approach for building large, complex hydrologic modeling systems. In contrast to more traditional software paradigms (i.e. procedural or object-oriented approaches), using component-based approaches allows individuals to construct autonomous modeling units that can be linked together through shared boundary conditions during a simulation run. One of the challenges in component-based modeling is designing a simple yet robust means for authoring model components. The Simple Model Wrapper (SMW) is an approach for efficiently creating standards-based, process-level hydrologic modeling components. Using this approach, a hydrologic process is implemented as a modeling component by:

<div style="float: right; margin: 1em">
![swm]({{site.baseurl}}/img/simple_model_wrapper.jpg){:height="300px" width="500px"}
<!-- <img src="{{ site.url }}img/simple_model_wrapper.jpg" width=500px height=300px alt="Simple Model Wrapper"> -->
</div>


* Authoring a configuration file that defines the properties of the component and 
* Creating a class with three methods that define the pre-run, runtime, and post-run behavior of the modeling component.


This work was presented in **Castronova and Goodall, 2010**, further information and source code for this project can be found <a href="https://code.google.com/p/smw/">here</a>.


