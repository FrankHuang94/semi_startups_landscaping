# Research Radar

## Top Papers by Commercialization Potential

| Paper | Venue | Categories | Score | Investor Relevance |
| --- | --- | --- | --- | --- |
| FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness | NeurIPS | inference_acceleration, memory_hbm_cxl_near_memory | 5 | IO-aware exact attention materially reduced memory traffic and became a core optimization in modern model stacks. |
| Efficient Memory Management for Large Language Model Serving with PagedAttention | SOSP | inference_acceleration, memory_hbm_cxl_near_memory | 5 | PagedAttention virtualizes KV-cache allocation and helped establish model-serving software as a strategic control point. |
| MLIR: Scaling Compiler Infrastructure for Domain Specific Computation | CGO | eda_compilers_runtimes_devtools, custom_asic_chiplets | 5 | MLIR provides reusable compiler infrastructure that has become foundational for heterogeneous and domain-specific hardware. |
| Pond: CXL-Based Memory Pooling Systems for Cloud Platforms | ASPLOS | memory_hbm_cxl_near_memory, pcie_cxl_retimers_connectivity | 5 | Demonstrates the system and fleet-level economic case for disaggregated CXL memory pooling. |
| MegaScale: Scaling Large Language Model Training to More Than 10,000 GPUs | NSDI | networking_switching_nic_dpu, datacenter_ai_accelerators | 5 | Shows that networking, topology, reliability, and observability become first-order product opportunities at frontier scale. |
| Eyeriss v2: A Flexible Accelerator for Emerging Deep Neural Networks on Mobile Devices | JSSC | edge_ai_iot_wearables, automotive_robotics_ai_silicon | 4 | The hierarchical mesh and sparse dataflow illustrate how edge accelerators can adapt to diverse neural-network shapes. |
| Timeloop: A Systematic Approach to DNN Accelerator Evaluation | ISPASS | datacenter_ai_accelerators, eda_compilers_runtimes_devtools | 4 | A systematic mapping and modeling framework lowers the cost of evaluating accelerator architectures and memory hierarchies. |
| Parallel convolutional processing using an integrated photonic tensor core | Nature | optical_interconnect_photonics_dsp, datacenter_ai_accelerators | 4 | Integrated photonic matrix operations show a path toward high-throughput, low-latency analog optical compute. |
| Cerebras-GPT: Open Compute-Optimal Language Models Trained on the Cerebras Wafer-Scale Cluster | arXiv | datacenter_ai_accelerators | 4 | Connects a differentiated accelerator architecture to reproducible model-training outcomes and an open model family. |
| TensorDIMM: A Practical Near-Memory Processing Architecture for Embeddings and Tensor Operations | MICRO | memory_hbm_cxl_near_memory, inference_acceleration | 4 | Near-memory processing for embeddings anticipated the bandwidth pressure now visible in recommenders and LLM serving. |

## Emerging Technology Themes

| Theme | Categories | Maturity | Investor Relevance |
| --- | --- | --- | --- |
| In-package optical I/O | optical_interconnect_photonics_dsp, advanced_packaging_chiplets_substrates | early_commercial | Electrical I/O power and reach constraints create a strategic transition point. |
| KV-cache memory hierarchy | inference_acceleration, memory_hbm_cxl_near_memory | early_commercial | Inference economics increasingly depend on memory capacity, movement, and scheduling. |
| Low-cost die-to-die connectivity | custom_asic_chiplets, advanced_packaging_chiplets_substrates | commercializing | Chiplet adoption needs interoperable links that work beyond the most expensive packages. |
| Ethernet scale-up and scale-out for AI | networking_switching_nic_dpu | commercializing | Open AI fabrics can challenge proprietary interconnects if congestion and collectives are solved. |
| Digital in-memory compute | inference_acceleration, edge_ai_iot_wearables | sampling | Digital approaches may capture memory-locality benefits with a more manufacturable risk profile than analog. |
| Glass substrates and interposers | advanced_packaging_chiplets_substrates | pilot | Large package size and high-frequency links are stressing organic substrate capabilities. |
| Two-phase direct-to-chip cooling | power_thermal_infrastructure | early_commercial | AI rack densities are pulling liquid cooling into mainstream datacenter design. |
| RISC-V as the control plane for AI silicon | riscv_processor_ip, datacenter_ai_accelerators | commercializing | RISC-V enables customizable control and vector processing around proprietary accelerators. |
| AI-native semiconductor design workflows | eda_compilers_runtimes_devtools | early_commercial | Engineering scarcity and design complexity create demand for automation beyond incumbent point tools. |
| Vertical and package-level power delivery | power_thermal_infrastructure, advanced_packaging_chiplets_substrates | pilot | Accelerator current density is making power delivery a package and silicon architecture problem. |

## Leading Researchers

| Researcher | Affiliation | Areas | Commercialization Score |
| --- | --- | --- | --- |
| Song Han | MIT | efficient AI, model compression, AI accelerators | 5 |
| Vivienne Sze | MIT | energy-efficient AI, computer architecture, video processing | 5 |
| Onur Mutlu | ETH Zurich | memory systems, processing-in-memory, computer architecture | 5 |
| David Patterson | UC Berkeley | RISC-V, computer architecture, domain-specific accelerators | 5 |
| Ramin Farjadrad | Eliyan | chiplets, SerDes, die-to-die interconnect | 5 |
| Vladimir Stojanovic | UC Berkeley / Ayar Labs | silicon photonics, integrated circuits, optical I/O | 5 |
| Nicholas Harris | Lightmatter | photonic computing, silicon photonics, AI systems | 5 |
| Kunle Olukotun | Stanford University / SambaNova Systems | parallel computing, dataflow, AI systems | 5 |
| Naveen Verma | Princeton University / EnCharge AI | in-memory compute, mixed-signal circuits, AI accelerators | 5 |
| Subhasish Mitra | Stanford University | 3D integration, nano systems, hardware reliability | 5 |
| Priyanka Raina | Stanford University | domain-specific architectures, accelerator design, EDA | 4 |
| Boris Murmann | University of Hawaii | mixed-signal IC, data converters, open-source silicon | 4 |

## Labs Producing Relevant Work

| Lab | Institution | Focus Areas | Startup Signals |
| --- | --- | --- | --- |
| HAN Lab | MIT | efficient AI, model compression, AI systems | open-source adoption, industry collaboration, alumni company formation |
| Energy-Efficient Multimedia Systems Group | MIT | edge AI, accelerators, energy-efficient computing | top-tier publications, industry collaboration |
| Berkeley AI Research and architecture ecosystem | UC Berkeley | RISC-V, AI systems, silicon photonics | RISC-V, Ayar Labs, open-source systems |
| Raina Systems Group | Stanford University | domain-specific architecture, accelerator design, EDA | industry collaboration, architecture tooling |
| Mitra Group | Stanford University | 3D integration, nano systems, reliability | patent activity, DARPA programs, commercializable integration |
| Verma Lab | Princeton University | in-memory compute, mixed-signal AI, sensing | EnCharge AI spinout, patents, industry collaboration |
| SAFARI Research Group | ETH Zurich | memory systems, processing-in-memory, reliability | open-source tools, patents, industry collaboration |
| imec | imec | advanced nodes, 3D integration, silicon photonics | venture spinouts, pilot lines, strategic partnerships |
| CEA-Leti | CEA | chiplets, photonics, advanced packaging | spinouts, patents, industrial transfer |
| Albany NanoTech Complex | NY CREATES | advanced semiconductor R&D, packaging, process integration | pilot infrastructure, industry consortia |

## Startup Formation Signals

See [hot research opportunities](views/hot_research_to_startup_opportunities.md).

## Research Workflow

1. Track repeated publication clusters, not isolated papers.
2. Separate scientific novelty from manufacturability and customer integration.
3. Link authors to patents, open-source adoption, grants, and industry collaborations.
4. Record a startup thesis only when a product wedge and buyer are identifiable.
