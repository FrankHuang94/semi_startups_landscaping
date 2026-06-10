from __future__ import annotations

from datetime import date
from typing import Any, Dict, List, Literal, Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator


class FlexibleModel(BaseModel):
    model_config = ConfigDict(extra="allow")


class Source(FlexibleModel):
    source_id: Optional[str] = None
    title: Optional[str] = None
    url: Optional[str] = None
    publisher: Optional[str] = None
    date_published: Optional[date] = None
    date_accessed: Optional[date] = None
    source_type: Optional[str] = None
    reliability: Optional[Literal["high", "medium", "low"]] = None
    notes: Optional[str] = None


class DataQuality(FlexibleModel):
    confidence_level: Literal["high", "medium", "low"] = "medium"
    last_company_update: Optional[date] = None
    last_verified: date
    missing_fields: List[str] = Field(default_factory=list)
    notes: Optional[str] = None


class Product(FlexibleModel):
    product_name: Optional[str] = None
    product_type: Optional[str] = None
    product_status: Literal[
        "concept", "research", "announced", "sampling", "shipping", "deployed",
        "discontinued", "unknown"
    ] = "unknown"
    target_workloads: List[str] = Field(default_factory=list)
    target_customers: List[str] = Field(default_factory=list)
    deployment_model: Optional[str] = None


class ProductProfile(FlexibleModel):
    products: List[Product] = Field(default_factory=list)


class BenchmarkClaim(FlexibleModel):
    claim: Optional[str] = None
    metric: Optional[str] = None
    workload: Optional[str] = None
    compared_against: Optional[str] = None
    independently_verified: bool = False
    source_id: Optional[str] = None


class TechnicalProfile(FlexibleModel):
    architecture: Optional[str] = None
    process_node: Optional[str] = None
    packaging: Optional[str] = None
    memory_interface: Optional[str] = None
    interconnect: Optional[str] = None
    software_stack: Optional[str] = None
    compiler_runtime: Optional[str] = None
    supported_frameworks: List[str] = Field(default_factory=list)
    manufacturing_dependencies: List[str] = Field(default_factory=list)
    technical_differentiation: Optional[str] = None
    benchmark_claims: List[BenchmarkClaim] = Field(default_factory=list)
    technical_risks: List[str] = Field(default_factory=list)


class ScoreSet(FlexibleModel):
    market_size: Optional[int] = Field(default=None, ge=1, le=5)
    timing: Optional[int] = Field(default=None, ge=1, le=5)
    technical_differentiation: Optional[int] = Field(default=None, ge=1, le=5)
    founder_quality: Optional[int] = Field(default=None, ge=1, le=5)
    customer_pull: Optional[int] = Field(default=None, ge=1, le=5)
    business_model_quality: Optional[int] = Field(default=None, ge=1, le=5)
    capital_efficiency: Optional[int] = Field(default=None, ge=1, le=5)
    competitive_intensity: Optional[int] = Field(default=None, ge=1, le=5)
    exit_potential: Optional[int] = Field(default=None, ge=1, le=5)
    strategic_scarcity: Optional[int] = Field(default=None, ge=1, le=5)
    overall_vc_priority: Optional[
        Literal["pass", "monitor", "watchlist", "active_diligence", "high_conviction"]
    ] = None


class Headquarters(FlexibleModel):
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None


class Company(FlexibleModel):
    company_id: str = Field(min_length=3)
    name: str = Field(min_length=1)
    legal_name: Optional[str] = None
    status: Literal["private", "public", "acquired", "shutdown", "stealth", "unknown"]
    website: Optional[str] = None
    hq: Headquarters
    founded_year: Optional[int] = Field(default=None, ge=1900, le=2100)
    primary_category: str
    secondary_categories: List[str] = Field(default_factory=list)
    technology_tags: List[str] = Field(default_factory=list)
    one_line_summary: Optional[str] = None
    investor_summary: Optional[str] = None
    problem_statement: Optional[str] = None
    solution_summary: Optional[str] = None
    product_profile: ProductProfile
    technical_profile: TechnicalProfile
    market_profile: Dict[str, Any]
    commercial_profile: Dict[str, Any]
    funding_profile: Dict[str, Any]
    team_profile: Dict[str, Any]
    competitive_landscape: Dict[str, Any]
    vc_investment_view: Dict[str, Any]
    strategic_scoring: ScoreSet
    relevance_to_qualcomm_or_strategics: Dict[str, Any]
    sources: List[Source] = Field(default_factory=list)
    data_quality: DataQuality

    @field_validator("secondary_categories")
    @classmethod
    def no_primary_duplicate(cls, values: List[str]) -> List[str]:
        return list(dict.fromkeys(values))


class Paper(FlexibleModel):
    paper_id: str
    title: Optional[str] = None
    authors: List[str] = Field(default_factory=list)
    institution_affiliations: List[str] = Field(default_factory=list)
    venue: Optional[str] = None
    publication_year: Optional[int] = None
    publication_date: Optional[date] = None
    url: Optional[str] = None
    arxiv_url: Optional[str] = None
    doi: Optional[str] = None
    research_category: List[str] = Field(default_factory=list)
    technology_tags: List[str] = Field(default_factory=list)
    abstract_summary: Optional[str] = None
    investor_relevance: Optional[str] = None
    technical_contribution: Optional[str] = None
    commercialization_potential: Dict[str, Any]
    startup_signal: Dict[str, Any]
    sources: List[Source] = Field(default_factory=list)
    data_quality: DataQuality


class Patent(FlexibleModel):
    patent_id: str
    title: Optional[str] = None
    patent_number: Optional[str] = None
    application_number: Optional[str] = None
    jurisdiction: Optional[str] = None
    filing_date: Optional[date] = None
    publication_date: Optional[date] = None
    grant_date: Optional[date] = None
    assignee: Optional[str] = None
    inventors: List[str] = Field(default_factory=list)
    research_category: List[str] = Field(default_factory=list)
    technology_tags: List[str] = Field(default_factory=list)
    patent_summary: Optional[str] = None
    claimed_invention_summary: Optional[str] = None
    investor_relevance: Optional[str] = None
    commercialization_signal: Dict[str, Any]
    sources: List[Source] = Field(default_factory=list)
    data_quality: DataQuality


class Researcher(FlexibleModel):
    researcher_id: str
    name: Optional[str] = None
    current_affiliation: Optional[str] = None
    prior_affiliations: List[str] = Field(default_factory=list)
    location: Optional[str] = None
    research_areas: List[str] = Field(default_factory=list)
    related_categories: List[str] = Field(default_factory=list)
    commercialization_signal: Dict[str, Any]
    sources: List[Source] = Field(default_factory=list)
    data_quality: DataQuality


class Investor(FlexibleModel):
    investor_id: str
    name: Optional[str] = None
    investor_type: Literal[
        "VC", "CVC", "growth_equity", "sovereign", "strategic", "family_office", "accelerator"
    ]
    website: Optional[str] = None
    hq: Headquarters
    semiconductor_thesis: Optional[str] = None
    ai_infrastructure_thesis: Optional[str] = None
    preferred_stage: List[str] = Field(default_factory=list)
    relevance_for_deal_sourcing: Dict[str, Any]
    sources: List[Source] = Field(default_factory=list)
    data_quality: DataQuality


class Transaction(FlexibleModel):
    transaction_id: str
    target_company: Optional[str] = None
    target_company_id: Optional[str] = None
    acquirer: Optional[str] = None
    acquirer_type: Literal["strategic", "private_equity", "financial_sponsor", "unknown"]
    target_categories: List[str] = Field(default_factory=list)
    announcement_date: Optional[date] = None
    close_date: Optional[date] = None
    transaction_status: Literal["rumored", "announced", "closed", "terminated", "unknown"]
    transaction_value_usd_m: Optional[float] = Field(default=None, ge=0)
    consideration_type: Literal["cash", "stock", "cash_stock", "undisclosed", "unknown"]
    strategic_rationale: Optional[str] = None
    technology_rationale: Optional[str] = None
    buyer_gap_filled: Optional[str] = None
    exit_readthrough_for_vc: Optional[str] = None
    valuation_readthrough: Optional[str] = None
    sources: List[Source] = Field(default_factory=list)
    data_quality: DataQuality


class RefreshLog(FlexibleModel):
    display_name: str
    file_path: str
    last_refreshed: date
    refreshed_by: str
    refresh_scope: Literal["full", "partial", "targeted", "source_check_only"]
    refresh_summary: Optional[str] = None
    open_questions: List[str] = Field(default_factory=list)
    next_refresh_recommendation: Optional[date] = None


MODEL_BY_KIND = {
    "company": Company,
    "paper": Paper,
    "patent": Patent,
    "researcher": Researcher,
    "investor": Investor,
    "transaction": Transaction,
    "refresh_log": RefreshLog,
}
