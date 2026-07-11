from typing import Union

from pssapi.enums import AllianceMembership

from ..models.enums import UserAllianceMembershipEncoded

ALLIANCE_MEMBERSHIP_ENCODED_TO_MEMBERSHIP = {
    UserAllianceMembershipEncoded.NONE: AllianceMembership.NONE,
    UserAllianceMembershipEncoded.CANDIDATE: AllianceMembership.CANDIDATE,
    UserAllianceMembershipEncoded.ENSIGN: AllianceMembership.ENSIGN,
    UserAllianceMembershipEncoded.LIEUTENANT: AllianceMembership.LIEUTENANT,
    UserAllianceMembershipEncoded.MAJOR: AllianceMembership.MAJOR,
    UserAllianceMembershipEncoded.COMMANDER: AllianceMembership.COMMANDER,
    UserAllianceMembershipEncoded.VICE_ADMIRAL: AllianceMembership.VICE_ADMIRAL,
    UserAllianceMembershipEncoded.FLEET_ADMIRAL: AllianceMembership.FLEET_ADMIRAL,
}

ALLIANCE_MEMBERSHIP_MEMBERSHIP_TO_ENCODED = {value: key for key, value in ALLIANCE_MEMBERSHIP_ENCODED_TO_MEMBERSHIP.items()}


def decode_alliance_membership(membership: Union[int, UserAllianceMembershipEncoded]) -> AllianceMembership:
    """Converts an `int` or `UserCreateAllianceMembership` enum into a `AllianceMembership`.

    Args:
        membership (Union[int, UserCreateAllianceMembership]): The alliance membership (member rank) to be decoded.

    Raises:
        ValueError: Raised, if parameter `membership` is `None` or not a valid value for the enum `UserCreateAllianceMembership`.
        TypeError: Raised, if parameter `membership` is not of type `int` or `UserCreateAllianceMembership`.

    Returns:
        AllianceMembership: The decoded alliance membership (member rank).
    """
    if membership is None:
        raise ValueError("The parameter `membership` must not be `None`!")

    if isinstance(membership, bool) or not isinstance(membership, (int, UserAllianceMembershipEncoded)):
        raise TypeError("The parameter `membership` must be of type `int` or `UserCreateAllianceMembership`!")

    if isinstance(membership, int):
        membership = UserAllianceMembershipEncoded(membership)

    return ALLIANCE_MEMBERSHIP_ENCODED_TO_MEMBERSHIP[membership]


def encode_alliance_membership(membership: Union[str, AllianceMembership]) -> int:
    """Converts a `str` or `AllianceMembership` enum into an `int`.

    Args:
        membership (Union[str, AllianceMembership]): The alliance membership (member rank) to be encoded.

    Raises:
        TypeError: Raised, if the parameter `membership` is not of type `str` or `AllianceMembership`.
        ValueError: Raised, if the parameter `membership` is `None` or not a valid value of the `StrEnum` `AllianceMembership`.

    Returns:
        int: An `int` representing an encoded `AllianceMembership` value.
    """
    if not membership:
        raise ValueError("Parameter `membership` must not be `None`!")

    if not isinstance(membership, (str, AllianceMembership)):
        raise TypeError("Parameter `membership` must be of type `str` or `AllianceMembership`!")

    if isinstance(membership, str):
        membership = AllianceMembership(membership)

    return ALLIANCE_MEMBERSHIP_MEMBERSHIP_TO_ENCODED[membership]
