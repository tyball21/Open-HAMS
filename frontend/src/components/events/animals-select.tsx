import { useAnimalStatus } from "@/api/queries";
import { API_URL } from "@/api/utils";
import { AnimalStatus } from "@/api/animals";
import { formatDate, formatTime } from "@/utils";
import { AnimalEventWithDetails } from "@/utils/types";
import { CheckCircle, XCircle } from "lucide-react";
import { LoadingDots } from "../icons";
import { Avatar, AvatarImage } from "../ui/avatar";
import { Button } from "../ui/button";
import { Label } from "../ui/label";
import { AvatarWithTooltip } from "./avatar-with-tooltip";
import { CustomSelect } from "./custom-select";

export function AnimalsSelect(props: {
  selectedAnimals: string[];
  setSelectedAnimals: (value: string[]) => void;
  animalsDetails?: AnimalEventWithDetails[];
  title?: string;
}) {
  const animals = useAnimalStatus();
  if (animals.isLoading) return <LoadingDots />;

  return (
    <CustomSelect
      label={props.title || "Animals"}
      placeholder="Search animals"
      options={animals.data!.map((animal_info: AnimalStatus) => ({
        value: animal_info.animal.id.toString(),
        label: animal_info.animal.name,
        toRender: (
          <>
            <Avatar className="size-5">
              <AvatarImage src={(() => {
                const imageField = (animal_info.animal as any)["image_filename"] || (animal_info.animal as any)["image"];
                return imageField ? `${API_URL}/static/animal_images/${imageField}` : undefined;
              })()} />
            </Avatar>
            <span className="font-extralightlight text-xs text-foreground">
              {animal_info.animal.name}
            </span>
            <span className="ml-auto">
              {animal_info.status === "available" ? (
                <div className="flex items-center gap-2">
                  <span className="text-green-400">Available</span>
                </div>
              ) : animal_info.status === "unavailable" ? (
                <div className="flex items-center gap-2">
                  <span className="text-xs">Unavailable</span>
                  <span className="w-[30px] text-wrap text-start text-[8px] leading-tight">
                    {animal_info.status_description}
                  </span>
                </div>
              ) : (
                <span className="text-xs">Checked Out</span>
              )}
            </span>
          </>
        ),
      }))}
      selected={props.selectedAnimals}
      setSelected={props.setSelectedAnimals}
      listElement={({ value }: { value: string }) => {
        const animal = animals.data!.find(
          (animal_info: AnimalStatus) => animal_info.animal.id.toString() === value,
        );

        const animalDetails = props.animalsDetails?.find(
          (animalDetails) => animalDetails.animal.id.toString() === value,
        );
        return (
          <AvatarWithTooltip src={(() => {
            const imageField = (animal?.animal as any)?.["image_filename"] || (animal?.animal as any)?.["image"];
            return imageField ? `${API_URL}/static/animal_images/${imageField}` : "";
          })()}>
            <div className="flex items-center gap-2">
              <Avatar className="size-8">
                <AvatarImage src={(() => {
                  const imageField = (animal?.animal as any)?.["image_filename"] || (animal?.animal as any)?.["image"];
                  return imageField ? `${API_URL}/static/animal_images/${imageField}` : undefined;
                })()} />
              </Avatar>
              <span className="text-md font-semibold">
                {animal?.animal.name}
              </span>
              <Button
                className="ml-auto"
                size={"xs"}
                onClick={(e) => {
                  e.preventDefault();

                  props.setSelectedAnimals(
                    props.selectedAnimals.filter((id) => id !== value),
                  );
                }}
              >
                Remove
              </Button>
            </div>

            {props.animalsDetails !== undefined && (
              <>
                <div className="flex items-center justify-between gap-2">
                  <Label className="text-xs font-light">
                    Checkout for Event:
                  </Label>
                  {animalDetails?.animal_event.checked_out ? (
                    <p>
                      {formatDate(animalDetails.animal_event.checked_out)} -
                      {formatTime(animalDetails.animal_event.checked_out)}
                    </p>
                  ) : (
                    <p>N/A</p>
                  )}
                </div>

                <div className="flex items-center justify-between gap-2">
                  <Label className="text-xs font-light">
                    Checkin for Event:
                  </Label>
                  {animalDetails?.animal_event.checked_in ? (
                    <p>
                      {`${formatDate(animalDetails.animal_event.checked_in)}`}-
                      {formatTime(animalDetails.animal_event.checked_in)}
                    </p>
                  ) : (
                    <p>N/A</p>
                  )}
                </div>
              </>
            )}

            <div className="">
              {animal?.status === "available" ? (
                <div className="grid gap-2">
                  <div className="flex items-center gap-2">
                    <CheckCircle className="size-4 text-green-500" />
                    <span className="text-sm">Available</span>
                  </div>
                  <p>{animal?.status_description}</p>
                </div>
              ) : animal?.status === "unavailable" ? (
                <div className="grid gap-2">
                  <div className="flex items-center gap-2">
                    <XCircle className="size-4 text-red-500" />
                    <span className="text-sm">Unavailable</span>
                  </div>
                  <p>{animal?.status_description}</p>
                </div>
              ) : (
                <div className="grid gap-2">
                  <div className="flex items-center gap-2">
                    <XCircle className="size-4" />
                    <span className="text-sm">Checked Out</span>
                  </div>
                  <p>{animal?.status_description}</p>
                </div>
              )}
            </div>
          </AvatarWithTooltip>
        );
      }}
    />
  );
}
