import { useState } from "react";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import axios from "axios";
import { useSession } from "next-auth/react";
import Modal from "@mui/joy/Modal";
import ModalClose from "@mui/joy/ModalClose";
import Sheet from "@mui/joy/Sheet";
import Box from "@mui/joy/Box";
import Button from "@mui/joy/Button";
import FormControl from "@mui/joy/FormControl";
import FormLabel from "@mui/joy/FormLabel";
import Input from "@mui/joy/Input";

export default function CreateCaseModal({ openModal, setOpenModal }) {
  const [open, setOpen] = useState(openModal);
  const session = useSession();
  const queryClient = useQueryClient();

  const [formData, setFormData] = useState({
    case_number: "",
    case_name: "",
    opposing_party: "",
    client: "",
    status: "active",
  });

  const mutation = useMutation({
    mutationFn: async (caseData) => {
      const response = await axios.post(
        `${process.env.NEXT_PUBLIC_API_URL}/cases`,
        caseData,
        {
          headers: {
            Authorization: `Bearer ${session?.data?.accessToken}`,
          },
        },
      );
      return response.data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({
        queryKey: ["cases"],
      });
      setFormData({
        case_number: "",
        case_name: "",
        opposing_party: "",
        client: "",
        status: "active",
      });
      onClose();
    },
    onError: (error) => {
      console.log(error?.response?.data?.message);
      alert(error?.response?.data?.message);
    },
  });

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value,
    });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    mutation.mutate(formData);
  };

  const onClose = () => {
    setOpen(false);
    setOpenModal(false);
  };

  return (
    <Modal
      aria-labelledby="modal-title"
      aria-describedby="modal-desc"
      open={open}
      onClose={onClose}
      sx={{ display: "flex", justifyContent: "center", alignItems: "center" }}
    >
      <Sheet
        variant="outlined"
        sx={{
          maxWidth: 500,
          borderRadius: "md",
          p: 3,
          boxShadow: "lg",
        }}
      >
        <ModalClose variant="plain" sx={{ m: 1 }} />
        <h2 id="modal-title" className="text-xl font-semibold mb-4">
          Create New Case
        </h2>

        <form onSubmit={handleSubmit}>
          <Box sx={{ display: "flex", flexDirection: "column", gap: 2 }}>
            <FormControl required>
              <FormLabel>Case Number</FormLabel>
              <Input
                placeholder="e.g., CASE-001"
                name="case_number"
                value={formData.case_number}
                onChange={handleInputChange}
              />
            </FormControl>

            <FormControl required>
              <FormLabel>Case Name</FormLabel>
              <Input
                placeholder="Enter case name"
                name="case_name"
                value={formData.case_name}
                onChange={handleInputChange}
              />
            </FormControl>

            <FormControl>
              <FormLabel>Opposing Party</FormLabel>
              <Input
                placeholder="enter name of opposing party"
                name="opposing_party"
                value={formData.opposing_party}
                onChange={handleInputChange}
              />
            </FormControl>

            <FormControl>
              <FormLabel>Client</FormLabel>
              <Input
                placeholder="Enter name of client"
                name="client"
                value={formData.client}
                onChange={handleInputChange}
              />
            </FormControl>

            <Box sx={{ display: "flex", gap: 2, justifyContent: "flex-end" }}>
              <Button variant="plain" color="neutral" onClick={onClose}>
                Cancel
              </Button>
              <Button
                variant="solid"
                color="primary"
                type="submit"
                loading={mutation.isPending}
              >
                Create Case
              </Button>
            </Box>
          </Box>
        </form>
      </Sheet>
    </Modal>
  );
}
