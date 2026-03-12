import Box from "@mui/joy/Box";
import Table from "@mui/joy/Table";
import ActionsDropdown from "./ActionsDropdown";
import Link from "next/link";
import { SquareArrowOutUpRight } from "lucide-react";

export default function CaseTable({ cases }) {
  return (
    <Box className="w-full m-2">
      <Table aria-label="table variants">
        <thead>
          <tr>
            <th>Case ID</th>
            <th>Case Number</th>
            <th>Case Name</th>
          </tr>
        </thead>
        <tbody>
          {cases?.map((caseItem) => (
            <tr
              className="text-black font-medium border-b border-blue-800"
              key={caseItem.id}
            >
              <td>{caseItem.id}</td>
              <td>{caseItem.case_number}</td>
              <td className="flex justify-between">
                {caseItem.case_name}
                <div className="flex gap-2 justify-center items-center">
                  <ActionsDropdown
                    caseId={caseItem.id}
                    status={caseItem.status}
                  />
                  <Link href={`/cases/${caseItem.id}`}>
                    <SquareArrowOutUpRight />
                  </Link>
                </div>
              </td>
            </tr>
          ))}
        </tbody>
      </Table>
    </Box>
  );
}
