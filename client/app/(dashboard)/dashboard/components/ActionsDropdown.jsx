import Menu from "@mui/joy/Menu";
import MenuButton from "@mui/joy/MenuButton";
import MenuItem from "@mui/joy/MenuItem";
import Dropdown from "@mui/joy/Dropdown";
import { Button } from "@mui/joy";
import { EllipsisVertical } from "lucide-react";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import axios from "axios";
import { useSession } from "next-auth/react";

export default function ActionsDropdown({ status, caseId }) {
  const queryClient = useQueryClient();
  const session = useSession();
  const mutation = useMutation({
    mutationFn: async (caseId) => {
      const response = await axios.patch(
        `${process.env.NEXT_PUBLIC_API_URL}/cases/${caseId}`,
        { status: status === "archive" ? "active" : "archive" },
        {
          headers: {
            Authorization: `Bearer ${session?.data?.accessToken}`,
          },
        },
      );

      return response.data;
    },
  });

  const handleClick = () => {
    mutation.mutate(caseId, {
      onSuccess: () => {
        queryClient.invalidateQueries({ queryKey: ["cases"] });
      },
      onError: (error) => {
        alert(error);
      },
    });
  };
  return (
    <Dropdown>
      <MenuButton variant="plain">
        <EllipsisVertical />
      </MenuButton>
      <Menu>
        <MenuItem onClick={handleClick}>
          {status === "archive" ? "Unarchive" : "Archive"}
        </MenuItem>
      </Menu>
    </Dropdown>
  );
}
