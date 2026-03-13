"use client";

import { useState } from "react";
import { useQuery, useMutation } from "@tanstack/react-query";
import { useSession } from "next-auth/react";
import axios from "axios";
import {
  ReactFlow,
  Background,
  Controls,
  ConnectionLineType,
} from "@xyflow/react";
import { GitFork, Network, Loader2 } from "lucide-react";
import "@xyflow/react/dist/style.css";
import dagre from "@dagrejs/dagre";

function buildGraph(entities, relationships) {
  const cols = Math.ceil(Math.sqrt(entities.length));
  const spacingX = 200;
  const spacingY = 100;
  const nodes = entities.map((e, i) => ({
    id: String(e.id),
    data: { label: `${e.name}` },
    position: {
      x: (i % cols) * spacingX,
      y: Math.floor(i / cols) * spacingY,
    },
    style: {
      background: "#eff6ff",
      border: "1px solid #93c5fd",
      borderRadius: 8,
      padding: "8px 12px",
      fontSize: 12,
    },
  }));

  const edges = relationships.map((r) => ({
    id: String(r.id),
    source: String(r.source_entity.id),
    target: String(r.target_entity.id),
    label: r.relationship_type,
    style: { stroke: "#93c5fd" },
    labelStyle: { fontSize: 10, fill: "#6b7280" },
  }));

  return { nodes, edges };
}

const nodeWidth = 172;
const nodeHeight = 36;

const getLayoutedElements = (nodes, edges, direction = "TB") => {
  const dagreGraph = new dagre.graphlib.Graph();
  dagreGraph.setDefaultEdgeLabel(() => ({}));
  dagreGraph.setGraph({
    rankdir: direction,
    nodesep: 150,
    ranksep: 150,
    marginx: 50,
    marginy: 50,
  });

  nodes.forEach((node) => {
    dagreGraph.setNode(node.id, { width: nodeWidth, height: nodeHeight });
  });

  edges.forEach((edge) => {
    dagreGraph.setEdge(edge.source, edge.target);
  });

  dagre.layout(dagreGraph);

  const newNodes = nodes?.map((node) => {
    const nodeWithPosition = dagreGraph.node(node.id);
    const newNode = {
      ...node,
      // We are shifting the dagre node position (anchor=center center) to the top left
      // so it matches the React Flow node anchor point (top left).
      position: {
        x: nodeWithPosition.x - nodeWidth / 2,
        y: nodeWithPosition.y - nodeHeight / 2,
      },
    };

    return newNode;
  });

  return { nodes: newNodes, edges };
};

export default function GraphPage({ caseId }) {
  const { data: session } = useSession();
  const [graphData, setGraphData] = useState(false);
  const [initialNodes, setInitialNodes] = useState([]);
  const [initialEdges, setInitialEdges] = useState([]);
  const { nodes: layoutedNodes, edges: layoutedEdges } = getLayoutedElements(
    initialNodes,
    initialEdges,
  );

  const headers = { Authorization: `Bearer ${session?.accessToken}` };
  const base = `${process.env.NEXT_PUBLIC_API_URL}/cases/${caseId}`;

  // Extract relationships mutation
  const extractMutation = useMutation({
    mutationFn: () => axios.get(`${base}/extract-relationships`, { headers }),
  });

  // Fetch entities + relationships then build graph
  const { isFetching, refetch } = useQuery({
    queryKey: [caseId, "graph"],
    enabled: false,
    queryFn: async () => {
      const [entitiesRes, relationshipsRes] = await Promise.all([
        axios.get(`${base}/entities`, { headers }),
        axios.get(`${base}/relationships`, { headers }),
      ]);

      const entities = entitiesRes.data;
      const relationships = relationshipsRes.data;
      const graph = buildGraph(entities, relationships);
      setInitialNodes(graph.nodes);
      setInitialEdges(graph.edges);
      if (!graph.nodes || !graph.edges) {
        alert(
          "No relationships found. You may have not uploaded cases files or extraction is in process. Please try again later",
        );
        return;
      }
      setGraphData(true);
      return graph;
    },
  });

  return (
    <div className="flex h-full w-full flex-col bg-white">
      {/* Header */}
      <header className="flex items-center justify-between border-b border-gray-200 bg-white px-8 py-5 shadow-sm">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Case Graph</h1>
          <p className="mt-1 text-sm text-gray-600">
            Visualize entity relationships in this case.
          </p>
        </div>

        <div className="flex items-center gap-3">
          {/* Step 1 - Extract */}
          <button
            onClick={() => extractMutation.mutate()}
            disabled={extractMutation.isPending}
            className="inline-flex items-center gap-2 rounded-xl border border-gray-300 bg-white px-4 py-2.5 text-sm font-medium text-gray-700 shadow-sm hover:bg-gray-50 transition disabled:opacity-60"
          >
            {extractMutation.isPending ? (
              <Loader2 size={16} className="animate-spin" />
            ) : (
              <GitFork size={16} />
            )}
            {extractMutation.isPending
              ? "Extracting..."
              : "Extract Relationships"}
          </button>

          {/* Step 2 - Generate */}
          <button
            onClick={() => refetch()}
            disabled={isFetching}
            className="inline-flex items-center gap-2 rounded-xl bg-blue-600 px-4 py-2.5 text-sm font-semibold text-white shadow-sm hover:bg-blue-700 transition disabled:opacity-60"
          >
            {isFetching ? (
              <Loader2 size={16} className="animate-spin" />
            ) : (
              <Network size={16} />
            )}
            {isFetching ? "Generating..." : "Generate Graph"}
          </button>
        </div>
      </header>

      {/* Graph */}
      <div className="">
        {!graphData ? (
          <div className="flex h-full flex-col items-center justify-center gap-3 text-center">
            <Network size={40} className="text-gray-300" />
            <p className="text-sm font-medium text-gray-500">No graph yet</p>
            <p className="text-xs text-gray-400 max-w-xs">
              First extract relationships, then generate the graph to visualize
              entity connections.
            </p>
          </div>
        ) : (
          <div className="w-3xl h-screen">
            <ReactFlow
              nodes={layoutedNodes}
              edges={layoutedEdges}
              connectionLineType={ConnectionLineType.SmoothStep}
              fitView
            >
              <Background />
            </ReactFlow>
          </div>
        )}
      </div>

      {/* Error states */}
      {extractMutation.isError && (
        <p className="px-8 py-3 text-sm text-red-600 border-t border-red-100 bg-red-50">
          ⚠️{" "}
          {extractMutation.error?.response?.data?.message ||
            "Extraction failed."}
        </p>
      )}
    </div>
  );
}
