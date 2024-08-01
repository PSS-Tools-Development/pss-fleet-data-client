from typing import Union

from pssapi.enums import AllianceMembership

from ..models.enums import UserAllianceMembershipEncoded


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

    match membership:
        case UserAllianceMembershipEncoded.NONE:
            return AllianceMembership.NONE
        case UserAllianceMembershipEncoded.CANDIDATE:
            return AllianceMembership.CANDIDATE
        case UserAllianceMembershipEncoded.ENSIGN:
            return AllianceMembership.ENSIGN
        case UserAllianceMembershipEncoded.LIEUTENANT:
            return AllianceMembership.LIEUTENANT
        case UserAllianceMembershipEncoded.MAJOR:
            return AllianceMembership.MAJOR
        case UserAllianceMembershipEncoded.COMMANDER:
            return AllianceMembership.COMMANDER
        case UserAllianceMembershipEncoded.VICE_ADMIRAL:
            return AllianceMembership.VICE_ADMIRAL
        case UserAllianceMembershipEncoded.FLEET_ADMIRAL:
            return AllianceMembership.FLEET_ADMIRAL


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

    match membership:
        case AllianceMembership.NONE:
            return int(UserAllianceMembershipEncoded.NONE)
        case AllianceMembership.CANDIDATE:
            return int(UserAllianceMembershipEncoded.CANDIDATE)
        case AllianceMembership.ENSIGN:
            return int(UserAllianceMembershipEncoded.ENSIGN)
        case AllianceMembership.LIEUTENANT:
            return int(UserAllianceMembershipEncoded.LIEUTENANT)
        case AllianceMembership.MAJOR:
            return int(UserAllianceMembershipEncoded.MAJOR)
        case AllianceMembership.COMMANDER:
            return int(UserAllianceMembershipEncoded.COMMANDER)
        case AllianceMembership.VICE_ADMIRAL:
            return int(UserAllianceMembershipEncoded.VICE_ADMIRAL)
        case AllianceMembership.FLEET_ADMIRAL:
            return int(UserAllianceMembershipEncoded.FLEET_ADMIRAL)
