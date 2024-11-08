import { Box, Flex, Icon, Text, useColorModeValue } from "@chakra-ui/react"
import { useQueryClient } from "@tanstack/react-query"
import { Link } from "@tanstack/react-router"
import { FiBriefcase, FiHome, FiSettings, FiUsers } from "react-icons/fi"

import type { UserPublic } from "../../client"

const orders = [
  { icon: FiHome, title: "Dashboard", path: "/" },
  { icon: FiBriefcase, title: "Orders", path: "/orders" },
  { icon: FiSettings, title: "User Settings", path: "/settings" },
]

interface SidebarOrdersProps {
  onClose?: () => void
}

const SidebarOrders = ({ onClose }: SidebarOrdersProps) => {
  const queryClient = useQueryClient()
  const textColor = useColorModeValue("ui.main", "ui.light")
  const bgActive = useColorModeValue("#E2E8F0", "#4A5568")
  const currentUser = queryClient.getQueryData<UserPublic>(["currentUser"])

  const finalOrders = currentUser?.is_superuser
    ? [...orders, { icon: FiUsers, title: "Admin", path: "/admin" }]
    : orders

  const listOrders = finalOrders.map(({ icon, title, path }) => (
    <Flex
      as={Link}
      to={path}
      w="100%"
      p={2}
      key={title}
      activeProps={{
        style: {
          background: bgActive,
          borderRadius: "12px",
        },
      }}
      color={textColor}
      onClick={onClose}
    >
      <Icon as={icon} alignSelf="center" />
      <Text ml={2}>{title}</Text>
    </Flex>
  ))

  return (
    <>
      <Box>{listOrders}</Box>
    </>
  )
}

export default SidebarOrders
