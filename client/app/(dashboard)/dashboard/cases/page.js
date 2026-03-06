"use client";

import { useEffect, useState, useMemo } from "react";
import { useQuery } from "@tanstack/react-query";
import axios, { all } from "axios";
import { useSession } from "next-auth/react";
import CaseTable from "../components/CaseTable";
import { FormControl, RadioGroup, Radio, Button } from "@mui/joy";
import CreateCaseModal from "../components/CreateCaseModal";
export default function CasesPage() {
  const session = useSession();
  const [filter, setFilter] = useState("all");

  const {
    data: allCases,
    isLoading,
    isError,
  } = useQuery({
    queryKey: ["cases"],
    queryFn: async () => {
      const response = await axios.get(
        `${process.env.NEXT_PUBLIC_API_URL}/cases`,
        {
          headers: {
            Authorization: `Bearer ${session?.data?.accessToken}`,
          },
        },
      );
      return response.data;
    },
  });

  const filteredCases = useMemo(() => {
    if (!allCases) return [];
    if (filter === "all") return allCases;
    return allCases.filter((c) => c.status === filter);
  }, [allCases, filter]);

  const onFilterChange = (e) => {
    setFilter(e.target.value);
  };

  const [openModal, setOpenModal] = useState(false);

  return (
    <div className="min-h-screen bg-white">
      {openModal && (
        <CreateCaseModal openModal={openModal} setOpenModal={setOpenModal} />
      )}
      <div className="p-6 max-w-5xl mx-auto">
        <div className="mb-6 flex items-cente justify-between">
          <div>
            <h1 className="text-2xl font-bold text-blue-800 tracking-tight">
              Cases
            </h1>
            <p className="mt-1 font-normal text-sm text-black">
              Manage and track all your cases in one place.
            </p>
          </div>
        </div>

        <div className="flex items-center justify-between">
          <FormControl orientation="horizontal">
            <RadioGroup
              orientation="horizontal"
              value={filter}
              onChange={onFilterChange}
            >
              <Radio label="all" value="all" />
              <Radio label="archive" value="archive" />
              <Radio label="active" value="active" />
            </RadioGroup>
          </FormControl>
          <Button onClick={() => setOpenModal(true)}>Create new case</Button>
        </div>

        <div>
          {!isLoading && (
            <>
              <CaseTable cases={filteredCases} />
              <p className="mt-3 text-sm text-black font-normal">
                Showing {filteredCases?.length || 0} of {allCases?.length} cases
              </p>
            </>
          )}
        </div>
      </div>
    </div>
  );
}
