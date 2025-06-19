# -*- coding: utf-8 -*-
# SPDX-License-Identifier: MIT
import json
import math
import logging
from typing import Dict, List, Any, Optional, Tuple, Set
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from collections import defaultdict

from langchain_core.tools import BaseTool, tool

from config.mystery_config import MysteryEventConfig, MysteryEventType
from tools.decorators import log_io, mystery_tool

logger = logging.getLogger(__name__)


@dataclass
class EventCorrelation:
    """事件关联"""
    event_id1: str
    event_id2: str
    correlation_type: str
    correlation_strength: float
    description: str
    timestamp: Optional[datetime] = None
    witnesses: List[str] = field(default_factory=list)
    sources: List[str] = field(default_factory=list)
    phenomena: List[str] = field(default_factory=list)
    keywords: List[str] = field(default_factory=list)
    correlation_factors: Dict[str, Any] = field(default_factory=dict)
    
    def get_timestamp_str(self) -> str:
        """获取时间戳字符串"""
        return self.timestamp.isoformat() if self.timestamp else ""


@dataclass
class MysteryEvent:
    """神秘事件数据结构"""
    event_id: str
    title: str
    description: str
    event_type: str
    timestamp: Optional[datetime] = None
    location: Optional[Dict[str, float]] = None
    phenomena: List[str] = field(default_factory=list)
    keywords: List[str] = field(default_factory=list)
    witnesses: List[str] = field(default_factory=list)
    sources: List[str] = field(default_factory=list)
    
    @property
    def id(self) -> str:
        """获取事件ID"""
        return self.event_id
    
    def get_timestamp_str(self) -> str:
        """获取时间戳字符串"""
        return self.timestamp.isoformat() if self.timestamp else ""
    
    def get_location_value(self, key: str) -> Optional[float]:
        """获取位置信息的特定值"""
        return self.location.get(key) if self.location else None
    
    def has_valid_timestamp(self) -> bool:
        """检查是否有有效的时间戳"""
        return self.timestamp is not None
    
    def has_valid_location(self) -> bool:
        """检查是否有有效的位置信息"""
        return (self.location is not None and
                "lat" in self.location and
                "lon" in self.location)


class CorrelationAnalyzer(BaseTool):
    """关联分析工具"""
    name: str = "correlation_analyzer"
    description: str = "Analyze correlations between mysterious events based on multiple factors."
    
    def __init__(self, config: Optional[MysteryEventConfig] = None):
        super().__init__()
        self.config = config or MysteryEventConfig()
        self._phenomenon_features = defaultdict(list)
    
    @property
    def phenomenon_features(self) -> Dict[str, List[str]]:
        return dict(self._phenomenon_features)
    
    def _run(self, events_data: str, correlation_types: Optional[List[str]] = None) -> str:
        """执行关联分析
        
        Args:
            events_data: JSON格式的事件数据
            correlation_types: 关联类型列表
            
        Returns:
            分析结果的JSON字符串
        """
        try:
            events = []
            data = json.loads(events_data)
            
            for event_data in data:
                try:
                    event = self._parse_event(event_data)
                    events.append(event)
                except Exception as e:
                    logger.error(f"Error parsing event: {str(e)}")
            
            if not correlation_types:
                correlation_types = ["temporal", "geographical", "phenomenological", 
                                   "witness", "media"]
            
            correlations = self.analyze_correlations(events, correlation_types)
            
            return json.dumps({
                "total_events": len(events),
                "correlation_types": correlation_types,
                "total_correlations": len(correlations),
                "correlations": [self._correlation_to_dict(c) for c in correlations]
            })
            
        except Exception as e:
            error_msg = f"Failed to analyze correlations. Error: {repr(e)}"
            logger.error(error_msg)
            return json.dumps({"error": error_msg})
    
    def _parse_event(self, event_data: Dict[str, Any]) -> MysteryEvent:
        """解析事件数据
        
        Args:
            event_data: 事件数据字典
            
        Returns:
            MysteryEvent实例
        """
        timestamp = None
        if "timestamp" in event_data:
            try:
                timestamp = datetime.fromisoformat(event_data["timestamp"])
            except (ValueError, TypeError):
                logger.warning(f"Invalid timestamp format for event {event_data.get('event_id')}")
        
        location = None
        if "location" in event_data:
            try:
                loc_data = event_data["location"]
                if isinstance(loc_data, dict) and "lat" in loc_data and "lon" in loc_data:
                    location = {
                        "lat": float(loc_data["lat"]),
                        "lon": float(loc_data["lon"])
                    }
            except (ValueError, TypeError, KeyError):
                logger.warning(f"Invalid location data for event {event_data.get('event_id')}")
        
        return MysteryEvent(
            event_id=event_data["event_id"],
            title=event_data.get("title", ""),
            description=event_data.get("description", ""),
            event_type=event_data.get("event_type", "unknown"),
            timestamp=timestamp,
            location=location,
            phenomena=event_data.get("phenomena", []),
            keywords=event_data.get("keywords", []),
            witnesses=event_data.get("witnesses", []),
            sources=event_data.get("sources", [])
        )
    
    def analyze_correlations(self, events: List[MysteryEvent], correlation_types: List[str]) -> List[EventCorrelation]:
        """分析事件之间的关联性
        
        Args:
            events: 事件列表
            correlation_types: 关联类型列表
            
        Returns:
            关联列表
        """
        correlations = []
        for i in range(len(events)):
            for j in range(i + 1, len(events)):
                for correlation_type in correlation_types:
                    correlation = self._analyze_single_correlation(events[i], events[j], correlation_type)
                    if correlation:
                        correlations.append(correlation)
        return correlations
    
    def _correlation_to_dict(self, correlation: EventCorrelation) -> Dict[str, Any]:
        """将关联对象转换为字典
        
        Args:
            correlation: EventCorrelation实例
            
        Returns:
            字典格式的关联数据
        """
        result = {
            "event_id1": correlation.event_id1,
            "event_id2": correlation.event_id2,
            "correlation_type": correlation.correlation_type,
            "correlation_strength": correlation.correlation_strength,
            "description": correlation.description,
            "witnesses": correlation.witnesses,
            "sources": correlation.sources,
            "phenomena": correlation.phenomena,
            "keywords": correlation.keywords,
            "correlation_factors": correlation.correlation_factors
        }
        
        if correlation.timestamp:
            result["timestamp"] = correlation.timestamp.isoformat()
            
        return result
    
    def _event_to_dict(self, event: MysteryEvent) -> Dict[str, Any]:
        """将事件转换为字典格式
        
        Args:
            event: MysteryEvent实例
            
        Returns:
            事件的字典表示
        """
        result = {
            "event_id": event.id,
            "event_type": event.event_type,
            "title": event.title,
            "description": event.description,
            "phenomena": event.phenomena,
            "keywords": event.keywords,
            "witnesses": event.witnesses,
            "sources": event.sources
        }
        
        if event.has_valid_timestamp():
            result["timestamp"] = event.get_timestamp_str()
            
        if event.has_valid_location():
            result["location"] = {
                "lat": event.get_location_value("lat"),
                "lon": event.get_location_value("lon")
            }
            
        return result
    
    def _safe_calculate_distance(self, event1: MysteryEvent, event2: MysteryEvent) -> Optional[float]:
        """安全计算两个事件之间的地理距离
        
        Args:
            event1: 第一个事件
            event2: 第二个事件
            
        Returns:
            距离（公里），如果无法计算则返回None
        """
        if not (event1.has_valid_location() and event2.has_valid_location()):
            return None
            
        lat1 = event1.get_location_value("lat")
        lon1 = event1.get_location_value("lon")
        lat2 = event2.get_location_value("lat")
        lon2 = event2.get_location_value("lon")
        
        if None in (lat1, lon1, lat2, lon2):
            return None
            
        assert isinstance(lat1, float) and isinstance(lon1, float)
        assert isinstance(lat2, float) and isinstance(lon2, float)
            
        return self._calculate_distance(lat1, lon1, lat2, lon2)
    
    def _calculate_distance(self, lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """计算两点之间的地理距离（哈弗辛公式）
        
        Args:
            lat1: 第一点纬度
            lon1: 第一点经度
            lat2: 第二点纬度
            lon2: 第二点经度
            
        Returns:
            距离（公里）
        """
        R = 6371  # 地球半径（公里）
        
        lat1_rad = math.radians(lat1)
        lat2_rad = math.radians(lat2)
        delta_lat = math.radians(lat2 - lat1)
        delta_lon = math.radians(lon2 - lon1)
        
        a = (math.sin(delta_lat / 2) ** 2 +
             math.cos(lat1_rad) * math.cos(lat2_rad) *
             math.sin(delta_lon / 2) ** 2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        
        return R * c
    
    def _safe_time_diff_days(self, event1: MysteryEvent, event2: MysteryEvent) -> Optional[int]:
        """安全计算两个事件之间的时间差（天数）
        
        Args:
            event1: 第一个事件
            event2: 第二个事件
            
        Returns:
            天数差值，如果无法计算则返回None
        """
        if not (event1.has_valid_timestamp() and event2.has_valid_timestamp()):
            return None
        
        assert event1.timestamp is not None
        assert event2.timestamp is not None
        
        return abs((event1.timestamp - event2.timestamp).days)
    
    def _analyze_single_correlation(self, event1: MysteryEvent, event2: MysteryEvent, 
                                  correlation_type: str) -> Optional[EventCorrelation]:
        """分析两个事件之间的特定类型关联
        
        Args:
            event1: 第一个事件
            event2: 第二个事件
            correlation_type: 关联类型
            
        Returns:
            关联实例，如果无关联则返回None
        """
        if correlation_type == "temporal":
            return self._analyze_temporal_correlation(event1, event2)
        elif correlation_type == "geographical":
            return self._analyze_geographical_correlation(event1, event2)
        elif correlation_type == "phenomenological":
            return self._analyze_phenomenological_correlation(event1, event2)
        elif correlation_type == "witness":
            return self._analyze_witness_correlation(event1, event2)
        elif correlation_type == "media":
            return self._analyze_media_correlation(event1, event2)
        return None
    
    def _analyze_temporal_correlation(self, event1: MysteryEvent, 
                                    event2: MysteryEvent) -> Optional[EventCorrelation]:
        """分析时间关联
        
        Args:
            event1: 第一个事件
            event2: 第二个事件
            
        Returns:
            时间关联实例，如果无关联则返回None
        """
        days_diff = self._safe_time_diff_days(event1, event2)
        if days_diff is None or days_diff > 30:  # 30天阈值
            return None
            
        strength = max(0.0, 1.0 - (days_diff / 30.0))
        
        return EventCorrelation(
            event_id1=event1.id,
            event_id2=event2.id,
            correlation_type="temporal",
            correlation_strength=strength,
            description=f"Events occurred within {days_diff} days",
            timestamp=event1.timestamp,  # 使用较早事件的时间戳
            correlation_factors={"days_difference": days_diff}
        )
    
    def _analyze_geographical_correlation(self, event1: MysteryEvent, 
                                        event2: MysteryEvent) -> Optional[EventCorrelation]:
        """分析地理关联
        
        Args:
            event1: 第一个事件
            event2: 第二个事件
            
        Returns:
            地理关联实例，如果无关联则返回None
        """
        distance = self._safe_calculate_distance(event1, event2)
        if distance is None or distance > 100:  # 100公里阈值
            return None
            
        strength = max(0.0, 1.0 - (distance / 100.0))
        
        return EventCorrelation(
            event_id1=event1.id,
            event_id2=event2.id,
            correlation_type="geographical",
            correlation_strength=strength,
            description=f"Events occurred within {distance:.1f} km",
            correlation_factors={"distance_km": distance}
        )
    
    def _analyze_phenomenological_correlation(self, event1: MysteryEvent, 
                                            event2: MysteryEvent) -> Optional[EventCorrelation]:
        """分析现象关联
        
        Args:
            event1: 第一个事件
            event2: 第二个事件
            
        Returns:
            现象关联实例，如果无关联则返回None
        """
        common_phenomena = set(event1.phenomena) & set(event2.phenomena)
        if not common_phenomena:
            return None
            
        strength = len(common_phenomena) / max(len(event1.phenomena), len(event2.phenomena))
        
        return EventCorrelation(
            event_id1=event1.id,
            event_id2=event2.id,
            correlation_type="phenomenological",
            correlation_strength=strength,
            description=f"Events share {len(common_phenomena)} phenomena",
            phenomena=list(common_phenomena),
            correlation_factors={
                "common_phenomena": list(common_phenomena),
                "phenomena_overlap": strength
            }
        )
    
    def _analyze_witness_correlation(self, event1: MysteryEvent, 
                                   event2: MysteryEvent) -> Optional[EventCorrelation]:
        """分析目击者关联
        
        Args:
            event1: 第一个事件
            event2: 第二个事件
            
        Returns:
            目击者关联实例，如果无关联则返回None
        """
        common_witnesses = set(event1.witnesses) & set(event2.witnesses)
        if not common_witnesses:
            return None
            
        strength = len(common_witnesses) / max(len(event1.witnesses), len(event2.witnesses))
        
        return EventCorrelation(
            event_id1=event1.id,
            event_id2=event2.id,
            correlation_type="witness",
            correlation_strength=strength,
            description=f"Events share {len(common_witnesses)} witnesses",
            witnesses=list(common_witnesses),
            correlation_factors={
                "common_witnesses": list(common_witnesses),
                "witness_overlap": strength
            }
        )
    
    def _analyze_media_correlation(self, event1: MysteryEvent, 
                                 event2: MysteryEvent) -> Optional[EventCorrelation]:
        """分析媒体来源关联
        
        Args:
            event1: 第一个事件
            event2: 第二个事件
            
        Returns:
            媒体关联实例，如果无关联则返回None
        """
        common_sources = set(event1.sources) & set(event2.sources)
        if not common_sources:
            return None
            
        strength = len(common_sources) / max(len(event1.sources), len(event2.sources))
        
        return EventCorrelation(
            event_id1=event1.id,
            event_id2=event2.id,
            correlation_type="media",
            correlation_strength=strength,
            description=f"Events share {len(common_sources)} media sources",
            sources=list(common_sources),
            correlation_factors={
                "common_sources": list(common_sources),
                "source_overlap": strength
            }
        )


@tool
@log_io
def analyze_event_correlations(
    events_data: str,
    correlation_types: Optional[List[str]] = None
) -> str:
    """分析神秘事件之间的关联关系
    
    Args:
        events_data: JSON格式的事件数据列表
        correlation_types: 要分析的关联类型列表，可选值：temporal, geographical, phenomenological, witness, media
    
    Returns:
        JSON格式的关联分析结果
    """
    try:
        analyzer = CorrelationAnalyzer()
        return analyzer._run(events_data, correlation_types)
    except Exception as e:
        error_msg = f"Failed to analyze event correlations. Error: {repr(e)}"
        logger.error(error_msg)
        return json.dumps({"error": error_msg}, ensure_ascii=False)


@tool
@log_io
def build_correlation_timeline(
    events_data: str,
    time_window_days: int = 30
) -> str:
    """构建关联事件时间线
    
    Args:
        events_data: JSON格式的事件数据列表
        time_window_days: 时间窗口（天）
    
    Returns:
        JSON格式的时间线数据
    """
    try:
        events_list = json.loads(events_data)
        analyzer = CorrelationAnalyzer()
        events = [analyzer._parse_event(event_data) for event_data in events_list]
        
        # 按时间排序
        events_with_time = [e for e in events if e.timestamp]
        events_with_time.sort(key=lambda x: x.timestamp or datetime.min)
        
        # 构建时间线
        timeline = []
        for event in events_with_time:
            timeline.append({
                "id": event.id,
                "title": event.title,
                "timestamp": event.get_timestamp_str(),
                "event_type": event.event_type,
                "location": event.location
            })
        
        # 分析时间聚集
        clusters = []
        current_cluster = []
        
        for i, event in enumerate(events_with_time):
            if not current_cluster:
                current_cluster.append(event)
            else:
                time_diff = analyzer._safe_time_diff_days(event, current_cluster[-1])
                if time_diff is not None and time_diff <= 7:
                    current_cluster.append(event)
                else:
                    if len(current_cluster) > 1:
                        clusters.append({
                            "start_time": current_cluster[0].get_timestamp_str(),
                            "end_time": current_cluster[-1].timestamp.isoformat(),
                            "event_count": len(current_cluster),
                            "event_ids": [e.id for e in current_cluster]
                        })
                    current_cluster = [event]
        
        # 处理最后一个聚集
        if len(current_cluster) > 1:
            clusters.append({
                "start_time": current_cluster[0].timestamp.isoformat(),
                "end_time": current_cluster[-1].timestamp.isoformat(),
                "event_count": len(current_cluster),
                "event_ids": [e.id for e in current_cluster]
            })
        
        return json.dumps({
            "timeline": timeline,
            "clusters": clusters,
            "total_events": len(timeline),
            "cluster_count": len(clusters)
        }, ensure_ascii=False)
        
    except Exception as e:
        error_msg = f"Failed to build correlation timeline. Error: {repr(e)}"
        logger.error(error_msg)
        return json.dumps({"error": error_msg}, ensure_ascii=False)


@tool
@log_io
def analyze_location_patterns(
    events_data: str,
    radius_km: float = 100.0
) -> str:
    """分析地理位置模式
    
    Args:
        events_data: JSON格式的事件数据列表
        radius_km: 聚集半径（公里）
    
    Returns:
        JSON格式的地理模式分析结果
    """
    try:
        events_list = json.loads(events_data)
        analyzer = CorrelationAnalyzer()
        events = [analyzer._parse_event(event_data) for event_data in events_list]
        
        # 筛选有位置信息的事件
        events_with_location = [e for e in events if e.location]
        
        if not events_with_location:
            return json.dumps({"error": "No events with location information"}, ensure_ascii=False)
        
        # 地理聚集分析
        clusters = []
        processed_events = set()
        
        for i, event1 in enumerate(events_with_location):
            if event1.id in processed_events:
                continue
            
            cluster_events = [event1]
            processed_events.add(event1.id)
            
            for j, event2 in enumerate(events_with_location):
                if i != j and event2.id not in processed_events:
                    distance = analyzer._calculate_distance(
                        event1.location["lat"], event1.location["lon"],
                        event2.location["lat"], event2.location["lon"]
                    )
                    
                    if distance <= radius_km:
                        cluster_events.append(event2)
                        processed_events.add(event2.id)
            
            if len(cluster_events) > 1:
                # 计算聚集中心
                center_lat = sum(e.location["lat"] for e in cluster_events) / len(cluster_events)
                center_lon = sum(e.location["lon"] for e in cluster_events) / len(cluster_events)
                
                clusters.append({
                    "center": {"lat": center_lat, "lon": center_lon},
                    "event_count": len(cluster_events),
                    "event_ids": [e.id for e in cluster_events],
                    "radius_km": radius_km,
                    "events": [{
                        "id": e.id,
                        "title": e.title,
                        "location": e.location,
                        "event_type": e.event_type
                    } for e in cluster_events]
                })
        
        # 热点区域分析
        hotspots = [cluster for cluster in clusters if cluster["event_count"] >= 3]
        
        return json.dumps({
            "location_clusters": clusters,
            "hotspots": hotspots,
            "total_events_with_location": len(events_with_location),
            "cluster_count": len(clusters),
            "hotspot_count": len(hotspots)
        }, ensure_ascii=False)
        
    except Exception as e:
        error_msg = f"Failed to analyze location patterns. Error: {repr(e)}"
        logger.error(error_msg)
        return json.dumps({"error": error_msg}, ensure_ascii=False)


@tool
@mystery_tool(max_retries=3)
def analyze_mystery_correlations(events_data: str) -> str:
    """分析神秘事件之间的关联关系
    
    Args:
        events_data: JSON格式的事件数据列表
        
    Returns:
        JSON格式的分析结果
    """
    analyzer = CorrelationAnalyzer()
    return analyzer._run(events_data)


@tool
@mystery_tool(max_retries=3)
def analyze_temporal_patterns(events_data: str) -> str:
    """分析神秘事件的时间模式
    
    Args:
        events_data: JSON格式的事件数据列表
        
    Returns:
        JSON格式的分析结果
    """
    analyzer = CorrelationAnalyzer()
    try:
        events = []
        data = json.loads(events_data)
        
        for event_data in data:
            event = analyzer._parse_event(event_data)
            events.append(event)
        
        events_with_time = [e for e in events if e.has_valid_timestamp()]
        events_with_time.sort(key=lambda x: x.timestamp or datetime.min)
        
        result = {
            "total_events": len(events),
            "events_with_timestamp": len(events_with_time),
            "timeline": [analyzer._event_to_dict(e) for e in events_with_time],
            "temporal_clusters": []
        }
        
        # 分析时间聚类（7天内发生的事件视为一个簇）
        current_cluster = []
        last_timestamp = None
        
        for event in events_with_time:
            if last_timestamp is None or (
                event.has_valid_timestamp() and 
                last_timestamp.has_valid_timestamp() and
                (event.timestamp - last_timestamp.timestamp).days <= 7
            ):
                current_cluster.append(event)
            else:
                if len(current_cluster) >= 2:
                    result["temporal_clusters"].append({
                        "start": current_cluster[0].get_timestamp_str(),
                        "end": current_cluster[-1].get_timestamp_str(),
                        "events": [analyzer._event_to_dict(e) for e in current_cluster]
                    })
                current_cluster = [event]
            last_timestamp = event
        
        # 处理最后一个簇
        if len(current_cluster) >= 2:
            result["temporal_clusters"].append({
                "start": current_cluster[0].get_timestamp_str(),
                "end": current_cluster[-1].get_timestamp_str(),
                "events": [analyzer._event_to_dict(e) for e in current_cluster]
            })
        
        return json.dumps(result)
        
    except Exception as e:
        logger.error(f"Error analyzing temporal patterns: {str(e)}")
        return json.dumps({"error": str(e)})


@tool
@mystery_tool(max_retries=3)
def analyze_geographical_patterns(events_data: str) -> str:
    """分析神秘事件的地理模式
    
    Args:
        events_data: JSON格式的事件数据列表
        
    Returns:
        JSON格式的分析结果
    """
    analyzer = CorrelationAnalyzer()
    try:
        events = []
        data = json.loads(events_data)
        
        for event_data in data:
            event = analyzer._parse_event(event_data)
            events.append(event)
        
        events_with_location = [e for e in events if e.has_valid_location()]
        
        result = {
            "total_events": len(events),
            "events_with_location": len(events_with_location),
            "locations": [],
            "clusters": []
        }
        
        # 收集所有有效位置
        for event in events_with_location:
            result["locations"].append({
                "event": analyzer._event_to_dict(event),
                "location": {
                    "lat": event.get_location_value("lat"),
                    "lon": event.get_location_value("lon")
                }
            })
        
        # 分析地理聚类（50公里内的事件视为一个簇）
        used_events = set()
        cluster_id = 1
        
        for event in events_with_location:
            if event.id in used_events:
                continue
                
            cluster = []
            for other in events_with_location:
                if other.id in used_events:
                    continue
                    
                distance = analyzer._safe_calculate_distance(event, other)
                if distance is not None and distance <= 50:
                    cluster.append(other)
                    used_events.add(other.id)
            
            if len(cluster) >= 2:
                # 计算簇的中心
                center_lat = 0.0
                center_lon = 0.0
                valid_points = 0
                
                for e in cluster:
                    lat = e.get_location_value("lat")
                    lon = e.get_location_value("lon")
                    if lat is not None and lon is not None:
                        center_lat += lat
                        center_lon += lon
                        valid_points += 1
                
                if valid_points > 0:
                    cluster_center = {
                        "lat": center_lat / valid_points,
                        "lon": center_lon / valid_points
                    }
                    result["clusters"].append({
                        "cluster_id": f"gc_{cluster_id}",
                        "center": cluster_center,
                        "radius": 50,
                        "event_count": len(cluster),
                        "events": [analyzer._event_to_dict(e) for e in cluster]
                    })
                    cluster_id += 1
        
        return json.dumps(result)
        
    except Exception as e:
        logger.error(f"Error analyzing geographical patterns: {str(e)}")
        return json.dumps({"error": str(e)})